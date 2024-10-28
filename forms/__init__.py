from . import auth, portfolio_forms, user_forms
from .auth import RegisterForm, LoginForm
from .portfolio_forms import HomePageContentForm,\
    ProjectsPageForm, ExperienceForm, EducationForm, SkillsForm, LanguageForm, ProjectsPageForm, ContactForm
from .user_forms import SocialMediaInfoForm, UpdateEmailForm,\
    UpdatePhoneForm, ChangePasswordForm, AboutMeForm


#TODO: import all the forms directly from the forms package from forms import RegisterForm, CreatePostForm
