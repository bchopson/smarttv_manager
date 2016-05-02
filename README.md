# smarttv_manager
Django project for managing smart TV content.

The TV Content Dashboard is a digital signage application to enable faculty and student organizations to manage the content of four LG smart TVs on campus. The dashboard is a Python Django application that exposes an administrative interface (/admin) and a REST API (/docs) for updating the TV content. The TVs are set to point to a particular endpoint and receive a JSON object containing the URLs and durations of each unit of content, or slide. The webpage on the TV cycles through the slides at the specified intervals. In addition, the application includes the Wagtail content management system to facilitate content creation.

### Contributing

The easiest way to contribute is to use the Vagrantfile provided. The port mapping will need to be changed for users on Linux or Mac systems.
