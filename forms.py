from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length

class TeamForm(FlaskForm):
    team_name = StringField('team name', validators=[DataRequired(), Length(min=4, max=255)])
    submit = SubmitField("submit")

class ProjectForm(FlaskForm):
    project_name = StringField('project name', validators=[DataRequired(), Length(min=4, max=255)])
    completed = BooleanField('completed?')
    team_id = SelectField("Team")
    description = TextAreaField('description')
    submit = SubmitField("submit")

    def update_teams(self, teams):
        self.team_id.choices = [ (team.id, team.team_name) for team in teams ]

class UserForm(FlaskForm):
    select_user = SelectField("Get all teams and projects related to:")
    submit = SubmitField("submit")

    def update_users(self, users):
        self.select_user.choices = [ (user.id, user.username) for user in users ]

class EditTeamForm(FlaskForm):
    team_id = SelectField("select team to change name: ")
    team_name = StringField(':', validators=[DataRequired(), Length(min=4, max=255)])
    submit = SubmitField("submit")

    def update_teams(self, teams):
        self.team_id.choices = [ (team.id, team.team_name) for team in teams ]

class EditProjectForm(FlaskForm):
    project_id = SelectField("select project to change information: ")

    project_name = StringField('project name')
    completed = BooleanField('completed?')
    team_id = SelectField("Team")
    description = TextAreaField('description')
    submit = SubmitField("submit")

    def update_projects(self, projects):
        self.project_id.choices = [ (project.id, project.project_name) for project in projects ]

    def update_teams(self, teams):
        self.team_id.choices = [ (team.id, team.team_name) for team in teams ]

class DeleteTeamForm(FlaskForm):
    team_id = SelectField("select team to delete: ")
    submit = SubmitField("Delete")

    def update_teams(self, teams):
        self.team_id.choices = [ (team.id, team.team_name) for team in teams ]

class DeleteProjectForm(FlaskForm):
    project_id = SelectField("select project to delete: ")
    submit = SubmitField("Delete")

    def update_projects(self, projects):
        self.project_id.choices = [ (project.id, project.project_name) for project in projects ]