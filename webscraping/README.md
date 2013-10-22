<h2>Setting Up</h2>
<p>This web application was built in Python on the Django web-framework.</p>
<p>Python version: 2.7.5<br>
Django version: 1.5.1</p>
<p>So after you've forked the repo it's time to make sure you have the proper environment in order to run the application.</p>
<p>Make sure you have pip installed: https://pypi.python.org/pypi/pip</p>
<p>Or if you live on the edge, you can easy_install it:</p>
<p><code>easy_install pip</code></p> 
<p>However, it is not recommended that you install pip using easy_install due to pip not using SSL for downloading packages from PyPI, and thus leaving users more vulnerable to security threats. </p>
<p>So now that you have pip, you can easily download all the required modules using our requirements.txt:</p>
<p><code>pip install -r requirements.txt</code></p>
<p>Note: you might want to set up a virtual environment, using <a href="http://www.virtualenv.org/en/latest/">virtualenv</a></p> 
<p>At this point, you should have Python 2.7, Django 1.5.1, and all the other modules required installed on your environment.</p>

<h2>How to start admin(scraper) side or client-facing side:</h2>
<p>So after everything is set up, cd into the directory of either the admin/client django project folder</p>
<p><code>cd /directory/of/djangoproject</code></p>
<p>The manage.py file acts as a wrapper around the django-admin.py file. The manage.py file can be utilized to host your application locally by running this command on the terminal:</p>
<p><code>python manage.py runserver</code></p>
<p>or for short, if you have the permissions:</p>
<p><code>./manage.py runserver</code></p>
<p>runserver by default runs on port 8000, so you can specify the IP and port by giving it another argument. For example:</p>

<p><code>./manage.py runserver 1337</code></p>
<p>runs application on port 127.0.0.1:1337</p> 

<p><code>./manage.py runserver 0.0.0.0:8888</code></p>
<p>runs application on all IPs your machine can support instead of only the loopback interface</p> 

<p>For more information on manage.py / django-admin.py the django website provides excellent documentation. https://docs.djangoproject.com/en/1.5/ref/django-admin/</p>
<p>Once your development server is running, access the IP through the browser, and now you should now be able to interact with the app.</p>

<h2>Admin Interface</h2>
![Oopsie](/assets/admin.png "Admin-1")
![Daisy](/assets/admin-2.png "Admin-2")

<h2>Client Interface</h2>
![Boo](/assets/client.png "Client-1")
![Wahhh](/assets/client-2.png "Client-2")

<h2>More...</h2>
<p>Look <a href="https://github.com/siqbal00/webscraping/wiki/Project-Overview">here</a> for further documentation on the overall project.</p>
