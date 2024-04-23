from flask import Flask, render_template, flash, redirect, url_for
from forms import TeamForm, ProjectForm, UserForm, EditTeamForm, EditProjectForm, DeleteTeamForm, DeleteProjectForm
from model import db, User, Team, Project, connect_to_db

app = Flask(__name__)

app.secret_key = "keep this secret"

user_id = 1

@app.route("/")
def home():
    teams = User.query.get(user_id).teams

    team_form = TeamForm()
    project_form = ProjectForm()
    project_form.update_teams(teams)
    user_form = UserForm()
    user_form.update_users(User.query.all())

    edit_team_form = EditTeamForm()
    edit_team_form.update_teams(teams)

    delete_team_form = DeleteTeamForm()
    delete_team_form.update_teams(teams)


    user = User.query.filter_by(id = user_id).first()

    edit_project_form = EditProjectForm()
    edit_project_form.update_teams(teams)

    delete_project_form = DeleteProjectForm()

    project_list = []
    for team in teams:
        project_list.extend(Project.query.filter_by(team_id = team.id).all())
    edit_project_form.update_projects(project_list)
    delete_project_form.update_projects(project_list)

    projects = Project.query.all()
    return render_template("home.html", team_form = team_form, project_form = project_form, user_form = user_form, 
                           delete_team_form = delete_team_form, edit_project_form = edit_project_form,
                           delete_project_form = delete_project_form, edit_team_form = edit_team_form, user = user, 
                           teams = teams, projects = projects)

@app.route("/add-team", methods=["POST"])
def add_team():
    team_form = TeamForm()

    if team_form.validate_on_submit():
        team_name = team_form.team_name.data

        if Team.query.filter_by(team_name=team_name).first():
            flash(f'Team: {team_name} already exists')
        else:
            new_team = Team(team_name, user_id)
            db.session.add(new_team)
            db.session.commit()

        return redirect(url_for("home"))
    else:
        print("Form failed to validate on submit.")
        return redirect(url_for("home"))
    
@app.route("/add-project", methods=["POST"])
def add_project():
    project_form = ProjectForm()
    project_form.update_teams(User.query.get(user_id).teams)

    if project_form.validate_on_submit():
        print(project_form.project_name.data)
        project_name = project_form.project_name.data
        description = project_form.description.data
        completed = project_form.completed.data
        team_id = project_form.team_id.data

        new_project = Project(project_name, completed, team_id, description = description)
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        print("Project not successfully added")
        return redirect(url_for("home"))
    
@app.route("/select-user", methods=["POST"])
def select_user():
    global user_id
    user_form = UserForm()
    # line would send a list of teams linked to user_id to update_teams function in projects to update the choices in team select
    # could be changed to get all projects or teams of the user_id so move this to if validate on submit, so it changes when you 
    # validate choice of user you wish to see
    user_form.update_users(User.query.all())
    # User.query.get(user_id).teams gives a list of all team objects that has the user
    # User.query.all() gives a list of all user objects
    # user_form.update_teams(User.query.get(user_id).teams)

    if user_form.validate_on_submit():
        print(user_form.select_user.data)
        # this line should change user_id variable to id of user we're trying to select
        # commented code should be using the id of the team from the selection field
        # team_id = project_form.team_id.data
        user_id = user_form.select_user.data

        # if it works, grab projects and teams that has the user_id

        return redirect(url_for("home"))
    else:
        print("Project not successfully added")
        return redirect(url_for("home"))

@app.route("/edit-team", methods=["POST"])
def edit_team():
    team_form = EditTeamForm()

    team_form.update_teams(User.query.get(user_id).teams)

    if team_form.validate_on_submit():
        team_name = team_form.team_name.data
        team_id = team_form.team_id.data
        team = Team.query.filter_by(id = team_id).first()

        team.team_name = team_name

        db.session.add(team)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        print("Form failed to validate on submit.")
        return redirect(url_for("home"))
    
@app.route("/edit-project", methods=["POST"])
def edit_project():
    project_form = EditProjectForm()

    teams = User.query.get(user_id).teams
    projects = []

    for team in teams:
        projects.extend(Project.query.filter_by(team_id = team.id).all())

    project_form.update_teams(User.query.get(user_id).teams)
    project_form.update_projects(projects)

    if project_form.validate_on_submit():
        project_id = project_form.project_id.data
        project = Project.query.filter_by(id = project_id).first()

        # edit project with the form's inputted values
        project.project_name = project_form.project_name.data
        project.description = project_form.description.data
        project.completed = project_form.completed.data
        project.team_id = project_form.team_id.data

        db.session.add(project)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        print("Form failed to validate on submit.")
        return redirect(url_for("home"))
    
@app.route("/delete-team", methods=["POST"])
def delete_team():
    team_form = DeleteTeamForm()

    team_form.update_teams(User.query.get(user_id).teams)

    if team_form.validate_on_submit():

        team_id = team_form.team_id.data
        team = Team.query.filter_by(id = team_id).first()
        if team.projects:
            flash(f'{team.team_name} still has projects assigned to them')
        else:
            db.session.delete(team)
            db.session.commit()
        return redirect(url_for("home"))
    else:
        print("Form failed to validate on submit.")
        return redirect(url_for("home"))
    
@app.route("/delete-project", methods=["POST"])
def delete_project():
    project_form = DeleteProjectForm()

    teams = User.query.get(user_id).teams
    projects = []

    for team in teams:
        projects.extend(Project.query.filter_by(team_id = team.id).all())

    project_form.update_projects(projects)

    if project_form.validate_on_submit():
        project_id = project_form.project_id.data
        project = Project.query.filter_by(id = project_id).first()

        db.session.delete(project)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        print("Form failed to validate on submit.")
        return redirect(url_for("home"))
    


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug = True)