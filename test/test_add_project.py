from model.project import Project
import string
import random

def random_name(prefix, maxlen):
    symbols = string.ascii_letters
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])

project = Project(name=random_name("project_", 5), status='release', view_state='public')

#первый способ - добавление с помощью json файла с нагенерируемыми проектами
def test_add_project(app, json_project):
    project = json_project
    old_projects = app.project.get_project_list()
    app.project.add_project(project)
    new_projects = app.project.get_project_list()
    assert len(old_projects) + 1 == len(new_projects)
    old_projects.append(project)
    # проверка сравнения старого и нового списка с добавлением элемента
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)

# второй способ - добавление с помощью рандомного имени проекта и soap
def test_add_project_soap(app):
    username = "administrator"
    password = "root"
    old_projects = app.soap.get_project_list(username, password)
    app.project.add_project(project)
    new_projects = app.soap.get_project_list(username, password)
    assert len(old_projects) + 1 == len(new_projects)
    old_projects.append(project)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)





