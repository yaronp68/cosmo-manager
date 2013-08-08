#/*******************************************************************************
# * Copyright (c) 2013 GigaSpaces Technologies Ltd. All rights reserved
# *
# * Licensed under the Apache License, Version 2.0 (the "License");
# * you may not use this file except in compliance with the License.
# * You may obtain a copy of the License at
# *
# *       http://www.apache.org/licenses/LICENSE-2.0
# *
# * Unless required by applicable law or agreed to in writing, software
# * distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.
# *******************************************************************************/

from cosmo.celery import celery
from cosmo.events import send_task
import tempfile
import os
from os import path
import sys
import subprocess
import urllib2
import errno

@celery.task
def install(**kwargs):
    pass


@celery.task
def start(__cloudify_id, **kwargs):
    send_task(__cloudify_id, "10.0.0.5", "flask status", "running")


@celery.task
def deploy_application(application_name, application_url, port=8080, **kwargs):
    response = urllib2.urlopen(application_url)
    application_path = path.join(tempfile.gettempdir(), 'flask-apps', application_name)

    try:
        os.makedirs(application_path)
    except OSError as e:
        if not (e.errno == errno.EEXIST):
            raise

    application_file = path.join(application_path, 'app.py')
    with open(application_file, "w") as f: 
        f.write(response.read())

    command = [sys.executable, application_file, str(port)]
    subprocess.Popen(command)
    # TODO: how deployed application node id is passed here?
    app_node_id = "???"
    send_task(app_node_id, "10.0.0.5", "flask app status", "running")


def test():
    deploy_application('my-crazy-app', 'http://localhost:8000/data/flask_app.py', 9000)
