#!/bin/sh

#
# I created this file because the updates for CWTA are infrequent, and every time I have to do them
# I've forgotten what commands I need to run to get the dev env up
#

echo Updating GCloud Components...
gcloud components update


# dev_appserver.py ~/code/cwta/redesign/website
# python3 /Users/gregmli/Applications/google-cloud-sdk/bin/dev_appserver.py ~/code/cwta/redesign/website
python3 ~/code/cwta/redesign/website/main.py

echo
printf "Would you like to deploy the latest version? [y/N]: "
read deploy_choice

case "$deploy_choice" in
  [yY] | [yY][eE][sS] )
    echo "Deploying..."
    gcloud app deploy app.yaml --stop-previous-version --promote
    ;;
  * )
    echo "Skipping deployment."
    ;;
esac
