import os
from functools import wraps
from flask import Flask, render_template, abort, request, redirect, url_for
from datetime import datetime, timedelta

# from google.cloud import datastore
from google.cloud import firestore
import zoneinfo as zi

app = Flask(__name__, static_url_path='')
timezone = zi.ZoneInfo('America/Los_Angeles')
datastore_client = firestore.Client()


class ClassDescription:
    def __init__(self, firestoreBundle, target_tz, id=None):
        self._id = id
        self._name = firestoreBundle["name"]
        self._description = firestoreBundle["description"]
        self._instructor = firestoreBundle["instructor"]
        self._isActive = ClassDescription.checkBooleanProperty(firestoreBundle, "isActive", True)
        self._isEnrollmentFull = ClassDescription.checkBooleanProperty(firestoreBundle, "isEnrollmentFull", False)
        self._tuition = firestoreBundle["tuition"]
        self._tuitionNotes = firestoreBundle["tuitionNotes"]

        # Firestore stores everything in UTC. Convert to a local timezone
        # for display purposes (Pacific time).
        #
        # Also break out startTime into a date-less time object for easier
        # sorting/display in the week calendar view. Firestore doesn't have
        # a time property, so start date and time are encoded into single
        # datetime object
        #
        # endTime's date is ignored; only the time is important
        self._target_tz = target_tz
        self._startDate = firestoreBundle["startTime"].astimezone(self.target_tz)
        self._startTime = self.startDate.time()
        self._endTime = firestoreBundle["endTime"].astimezone(self.target_tz)
        if "alternateEndTime" in firestoreBundle:
            self._alternateEndTime = firestoreBundle["alternateEndTime"].astimezone(self.target_tz)

        self._scheduleNotes = firestoreBundle["scheduleNotes"]
    
    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name
    
    @property
    def description(self):
        return self._description
             

    @property
    def instructor(self):
        return self._instructor
    
    @property
    def isActive(self):
        return self._isActive
    
    @property
    def isEnrollmentFull(self):
        return self._isEnrollmentFull
    
    @property
    def tuition(self):
        return self._tuition
    
    @property
    def tuitionNotes(self):
        return self._tuitionNotes

    @property
    def target_tz(self):
        return self._target_tz
    
    @property
    def startDate(self):
        return self._startDate
    
    @property
    def startTime(self):
        return self._startTime
    
    @property
    def endTime(self):
        return self._endTime
    
    @property
    def alternateEndTime(self):
        return self._alternateEndTime
    
    @property
    def scheduleNotes(self):
        return self._scheduleNotes

    def isStarted(self):
        return self.startDate - timedelta(days=7) < datetime.now(self.target_tz)

    # helper for firestore booleans which may not be defined in the bundle
    def checkBooleanProperty(c, key, defaultIfNull=False):
        if key not in c:
            return defaultIfNull
        
        return c[key]



@app.route('/<page>')
def render(page):
    valid_templates = ['index', 'classes', 'instructors', 'chen', 'yang', 'resources', 'czl2016']
    template = page.lower()
    classes = fetchAllClasses()
    currentDate = datetime.now(timezone)
    newClasses = getNewClasses(classes, currentDate)

    if template in valid_templates:
        return render_template(template + '.html', 
                               now = currentDate,
                               tz=timezone,
                               classes=classes,
                               newClasses=newClasses)
    abort(404)

                
def getNewClasses(classes, currentDate):
    newClasses = {}
    for c in classes:
        if not(c.isStarted()) and not c.isEnrollmentFull:
            year = c.startDate.year
            if year not in newClasses:
                newClasses[year] = []

            newClasses[year].append(c)
    
    return newClasses



def fetchAllClasses(include_inactive=False):
    query = datastore_client.collection("class_schedules").order_by("startTime")

    docs = list(query.stream())

    # some day this filtering should be re-implemented in the query. But Google makes it way too
    # hard. Can't do it without creating an index and some other BS. The documentation
    # also sucks - not sure how to express "IS NULL OR != TRUE"
    #
    # classes = list(map(lambda d: d.to_dict(), docs))
    classes = []
    for d in docs:
        c = ClassDescription(d.to_dict(), timezone, d.id)

        if include_inactive or c.isActive:
            classes.append(c)
    
    return classes

def requires_local(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Block access completely if running in App Engine production
        if os.environ.get('GAE_ENV') == 'standard':
            abort(404)
        return f(*args, **kwargs)
    return decorated

@app.route('/admin/schedule')
@requires_local
def admin_schedule():
    classes = fetchAllClasses(include_inactive=True)
    classes.sort(key=lambda c: (not c.isActive, c.startDate.weekday(), c.startTime))
    return render_template('admin_schedule.html', classes=classes)

@app.route('/admin/schedule/edit/<id>')
@requires_local
def admin_schedule_edit(id):
    classes = fetchAllClasses(include_inactive=True)
    classes.sort(key=lambda c: (not c.isActive, c.startDate.weekday(), c.startTime))
    class_edit = next((c for c in classes if c.id == id), None)
    return render_template('admin_schedule.html', classes=classes, class_edit=class_edit)

@app.route('/admin/schedule/save', methods=['POST'])
@requires_local
def admin_schedule_save():
    id = request.form.get('id')
    
    start_date = request.form.get('startDate')
    start_time = request.form.get('startTime')
    
    start_dt = None
    if start_date and start_time:
        dt = datetime.strptime(f"{start_date} {start_time}", '%Y-%m-%d %H:%M')
        start_dt = dt.replace(tzinfo=timezone)
    
    # Combine start date with end times
    def combine_time(base_dt, time_str):
        if not base_dt or not time_str: return None
        t = datetime.strptime(time_str, '%H:%M').time()
        return base_dt.replace(hour=t.hour, minute=t.minute)

    data = {
        "name": request.form.get('name'),
        "description": request.form.get('description'),
        "instructor": request.form.get('instructor'),
        "isActive": request.form.get('isActive') == 'true',
        "isEnrollmentFull": request.form.get('isEnrollmentFull') == 'true',
        "tuition": request.form.get('tuition'),
        "tuitionNotes": request.form.get('tuitionNotes'),
        "scheduleNotes": request.form.get('scheduleNotes'),
        "startTime": start_dt,
        "endTime": combine_time(start_dt, request.form.get('endTime')),
        "alternateEndTime": combine_time(start_dt, request.form.get('alternateEndTime'))
    }
    
    # Remove None values to avoid Firestore errors or overwriting with null
    data_to_save = {k: v for k, v in data.items() if v is not None}

    if id:
        datastore_client.collection("class_schedules").document(id).set(data_to_save)
    else:
        datastore_client.collection("class_schedules").add(data_to_save)

    return redirect('/admin/schedule')

@app.route('/')
def root():
    return render('index')


if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host="127.0.0.1", port=8080, debug=True)
