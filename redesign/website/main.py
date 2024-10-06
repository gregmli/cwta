from flask import Flask, render_template, abort
from datetime import datetime, timedelta

# from google.cloud import datastore
from google.cloud import firestore
import zoneinfo as zi

app = Flask(__name__, static_url_path='')
timezone = zi.ZoneInfo('America/Los_Angeles')
datastore_client = firestore.Client()


class ClassDescription:
    def __init__(self, firestoreBundle, target_tz):
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



def fetchAllClasses():
    query = datastore_client.collection("class_schedules").order_by("startTime")

    docs = list(query.stream())

    # some day this filtering should be re-implemented in the query. But Google makes it way too
    # hard. Can't do it without creating an index and some other BS. The documentation
    # also sucks - not sure how to express "IS NULL OR != TRUE"
    #
    # classes = list(map(lambda d: d.to_dict(), docs))
    classes = []
    for d in docs:
        c = ClassDescription(d.to_dict(), timezone)

        if c.isActive:
            classes.append(c)
    
    return classes

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

