executive
=========

A proof of concept for an GUI re-imagination of the original executive.

Roadmap
=========
**Step -1:**

Try to revert the fact that we sold Executive, as it's not a product ready for sale. This way we prevent the cost of
developing it.

Investigate if there are other product currently not fit for sale, to prevent this situation occuring again.

**Step 0:**

Investigate the original documentation of Executive.

Investigate what the description is of Executive in the contact we sold it in.

Investigate why/how current users use Executive.

Investigate what feedback is available about Executive.

Investigate what other products are part of the set of tools Executive was included in.

These steps are needed to create a product that actually fits expectation of the clients.

Acquire the styling of GBN to make the proof of concept fit in.

**Step 0.5**:
The board of directions should approve the Proof of concept

**Step 1:**

Create a clear set of requirements (or expectations) and vision for Executive. (Which likely includes: An online
database with user authentication, an actual date input field, multiple users being able to share project, a more
complete ui, console support for existing customers, protection against sql injections, an automated installation and
tests. )

Move a senior Dev with experience with Azure & CI/CD from one of the other teams to lead this team.

Additionally add an UI designer if one is not already present, the GUI aspect is crucial for the succes of Executive

The Team originally responsible for this project should be trained in at least CI/CD.

**Step 2:**

Create a minimum viable product including all base functionalities current clients use.

Create an UI design that fullfills the role of decide.py

Create an executable that installs the product as an stand-alone desktop app. (Or go fully web-app)

**Step 3:**

Consider whether the minimum viable product is able to compete with existing product and be profitable.

Create automated tests for the minimum viable product

Consider integration with other products.

**Testing strategy:**

I would approach this in three ways (besides general testing):

Database queries should be tested to work properly

Buttons should be tested to trigger the correct Database queries

A test should be done before release that all functionalities work in the UI.

**Installation**
=========

Install Python 3.8

**Make sure your pythonpath contains the directory you just pulled**

unix: `export PYTHONPATH=/path/to/executive`

windows: `set export PYTHONPATH=/path/to/executive`

**Install dependencies**

run setup.py

**Usage**
=========

Right-clicking an action switches it completion status. Beware: Removing the orignal projects/actions will not save as
the demo database is reset on each run.
