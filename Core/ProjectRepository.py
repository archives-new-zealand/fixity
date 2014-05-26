#!/usr/bin/env python
from Core import SharedApp

class ProjectRepository(object):
    def __init__(self):
        self.Fixity = SharedApp.SharedApp.App

    def getAll(self):
        return self.Fixity.Database.getProjectInfo()

    def getSingleProject(self, project_name):
        try:
            selected_project_object = self.Fixity.ProjectsList[project_name]
            return selected_project_object
        except:
            return False