from selenium.webdriver.support.ui import Select
from model.project import Project

class ProjectHelper:

    def __init__(self, app):
        self.app = app

    def add_project(self, project):
        wd = self.app.wd
        self.open_manage_projects_page()
        # открыть форму создания проекта
        wd.find_element_by_xpath("//input[@value='Create New Project']").click()
        # заполнить поля
        self.fill_project_form(project)
        # создать проект
        wd.find_element_by_xpath("//input[@value='Add Project']").click()
        self.app.open_home_page()

    def fill_project_form(self, project):
        wd = self.app.wd
        self.change_field_value("name", project.name)
        wd.find_element_by_name("status").click()
        Select(wd.find_element_by_name("status")).select_by_visible_text(project.status)
        wd.find_element_by_name("view_state").click()
        Select(wd.find_element_by_name("view_state")).select_by_visible_text(project.view_state)
        if not project.inherit_global_categories:
            wd.find_element_by_name("inherit_global").click()
        self.change_field_value("description", project.description)

    def change_field_value(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    def select_project_by_id(self, project_id):
        wd = self.app.wd
        wd.find_element_by_css_selector("a[href='manage_proj_edit_page.php?project_id=%s']" % project_id).click()

    def delete_project_by_id(self, id):
        wd = self.app.wd
        self.open_manage_projects_page()
        self.select_project_by_id(id)
        print("id = %s was deleted" % id)
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()
        self.project_cache = None

    project_cache = None

    def get_project_list(self):
        wd = self.app.wd
        self.open_manage_projects_page()
        self.project_cache = []
        all_tables = wd.find_elements_by_xpath("//table[@class='width100']")
        table = all_tables[1]
        rows = table.find_elements_by_xpath(".//tr[contains(@class, 'row')]")
        del rows[0]
        for element in rows:
            cells = element.find_elements_by_tag_name("td")
            name = cells[0].text
            description_text = cells[4].text
            id_link = wd.find_element_by_link_text(name).get_attribute("href")
            id_index = id_link.index('=') + 1
            id = id_link[id_index:]
            self.project_cache.append(Project(id=id, name=name, description=description_text))
        return list(self.project_cache)

    def open_manage_projects_page(self):
        wd = self.app.wd
        wd.find_element_by_xpath("//a[contains(@href, '/mantisbt-1.2.20/manage_overview_page.php')]").click()
        wd.find_element_by_link_text("Manage Projects").click()

