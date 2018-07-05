tator2
======

An online collaborative image annotation tool

**License**: GPLv3


Settings
--------

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).


Basic Commands
--------------

**Setting up for local development**:

You should have Python (Preferably some virtualenv), yarn, and PostgreSQL installed.  
    
    cd tator2                              # get into our working directory (note: not tator2/tator2)
    pip install -r requirements/local.txt  # install python dependancies
    yarn install                           # install node modules
    createdb tator2                        # create a postgresql database
    python manage.py migrate               # initialize the database

Then, for the email backend, we use Mailhog. So:

1. [Download Mailhog for your OS](https://github.com/mailhog/MailHog/releases), 

2. Rename the build to MailHog.

3. Copy the file to the project root (`tator2/`)

4. Make it executable: `chmod +x MailHog`

5. Open another terminal at `tator2/` and run `./MailHog`

6. Test it out at: `http://127.0.0.1:8025/`

(In production we use [MailGun](https://www.mailgun.com/))

**Running locally**: 

Start a development server: `python manage.py runserver`.

Watch the frontend react files and automatically update when they change: `yarn start labelsquad`.

Make a production-ready build of the frontend: `yarn build <app to build, leave blank for default>`.

Start the Node.js render server for server-side rendering of React components: `yarn render`. (By default this is not used in development, but if you set `REACT.RENDER` to `True` in `config/base.py`, you can test it out. Note that you must restart the render server every time one of your component's source changes, as they are cached)


Setting Up Your Users
---------------------

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Test coverage
-------------

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run manage.py test
    $ coverage html
    $ open htmlcov/index.html