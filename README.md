# DjangoWebsite

**Introduction**</br>
I created a sample blog-like website using Django, Python, Javascript, Bootstrap, CSS.
The project was started as an introduction to Django, learning to make use of its built in tools such as the database, signals, models, and template rendering.
This website allows users to create an account where they can then upload a media file. The media file can either be an image, a GIF, or a video, along with a description for their post. Every media upload by all users will be displayed in the 'recent activity' page, where any logged in or anonymous user can view the post. The media post can then be clicked on for a larger picture or video, where any user can view comments on that post and logged in users can comment on the media post. Logged in users can also delete their own media posts or their own comments. Users can also click on a person's name to view their profile page. The profile page comes with a user's display picture as well as a description for themselves. The profile page also show's the user's feed which shows their recent uploads and comments. Lastly, a logged in user can edit their own profile, changing their username, description, or change the display picture.

**How to Use**</br>
This project requires installation of the modules shown in *requirements.txt*.</br>
The server is started using `python manage.py runserver`.</br>
A superuser/admin account can be created using `python manage.py createsuperuser`.</br>
A sample json file *media_test_data.json* can be loaded into the database once an account has been made using `python manage.py loaddata media_test_data`.</br>
The sample file includes 4 posts, which the different types of media files that can be uploaded to the website.

**Credit**</br>
Big thanks to Corey Schafer's Django Tutorial playlist as a reference point for this project.

**License**<br>
MIT License

Copyright (c) 2021 Ernest Chow

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
