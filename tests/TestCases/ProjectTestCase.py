# -*- coding: UTF-8 -*-
'''
Created on May 14, 2014

@author: Furqan Wasi <furqan@avpreserve.com>
'''


# built-in libraries
import unittest
import os
import sys

# Custom libraries

from AllFixture.ProjectFixtures import ProjectFixtures
from Core import ProjectCore
from AllFixture.EmailFixtures import EmailFixtures

import ExpectedResults as ExpectedResults
import FailedMessages as FailedMessages

import AllFixture.helper as helper
sys.path.append(helper.setImportBaseBath())

import Main


class ProjectTestCase(object):


    def __init__(self):
        self.App = Main.Main()
        self.project_fixtures = ProjectFixtures()
        pass

    def run_project(self, project_name):
        """
        Create New Project
        @param project_name:  project name to be ran
        @return:
        """
        
        print('Test Run Project.........!')
        self.project_fixtures.load_verification_algorithm_data()

        self.project_fixtures.create_new_project(project_name)

        project_information = self.App.LaunchCLI(project_name, 'test')
        try:
            self.project_fixtures.delete_testing_data()
        except:
            pass

        print("---------------------------------------------------------------------\n")
        return [project_information['created'], ExpectedResults.ProjectTestCaseExpectedResult['run_project'], FailedMessages.ProjectTestCaseFailMessages['run_project']]

    def delete_project(self, project_name):
        """
        Delete Project

        @param project_name: project name to be Deleted
        @return List:
        """
        print('Test Delete Project.........!')

        self.project_fixtures.create_new_project(project_name)
        project_core = self.App.Fixity.ProjectRepo.getSingleProject(project_name)

        deleted_project_id = project_core.getID()
        deleted_project_Title = project_core.getTitle()

        project_core.Delete()

        project_core_deleted = self.App.Fixity.ProjectRepo.getSingleProject(deleted_project_Title)
        flag = True
        try:
            project_core_deleted.getID()

            flag = False
        except:
            pass

        try:
            project_core_deleted.getID()
            project_core_deleted.getTitle()
            flag = False
        except:
            pass

        result_project = self.App.Fixity.Database.getProjectInfo(deleted_project_Title)
        result_project_detail = self.App.Fixity.Database.getVersionDetailsLast(deleted_project_id)
        if len(result_project) > 0:
            flag = False

        if len(result_project_detail) > 0:
            flag = False

        print("---------------------------------------------------------------------\n")
        return [flag, ExpectedResults.ProjectTestCaseExpectedResult['delete_project'], FailedMessages.ProjectTestCaseFailMessages['delete_project']]

    def change_project_name(self, project_name, new_project):
        """
        Change Project Name

        @param project_name: project name to be Changed
        @param new_project: project name to be changed with
        """

        flag = True
        print('Test Change Project Name .........!')
        self.project_fixtures.create_new_project(project_name)

        project_core = self.App.Fixity.ProjectRepo.getSingleProject(project_name)
        project_core.changeProjectName(project_name, new_project)
        project_core_new = self.App.Fixity.ProjectRepo.getSingleProject(new_project)

        try:
            project_core_new.getID()
            project_core_new.getTitle()
        except:
            flag = False

        try:
            self.project_fixtures.delete_testing_data()
        except:
            pass

        print("---------------------------------------------------------------------\n")
        return [flag, ExpectedResults.ProjectTestCaseExpectedResult['change_project_name'], FailedMessages.ProjectTestCaseFailMessages['change_project_name']]

    def save_project(self, project_name):
        """
        Save Project

        @param project_name: project name to be Saved
        """
        print('Test Save Project .........!')
        flag = False

        #try:
        self.project_fixtures.create_new_project(project_name)
        project_core = self.App.Fixity.ProjectRepo.getSingleProject(project_name)
        project_core.Save()
        flag = True
        #except:
        #    print(Exception.message)
        #    flag = False
        print(flag)
        try:
            self.project_fixtures.delete_testing_data()
        except:
            pass

        print("---------------------------------------------------------------------\n")
        return [flag, ExpectedResults.ProjectTestCaseExpectedResult['save_project'], FailedMessages.ProjectTestCaseFailMessages['save_project']]

    def change_algorithm(self, project_name):
        """
        Change Algorithm

        @param project_name: project name to be Changed Algorithm
        """

        print('Test Change Project Algorithm .........!')

        algo_value_selected = 'md5'
        flag = True
        self.project_fixtures.load_verification_algorithm_data()
        self.project_fixtures.create_new_project(project_name)

        project_core = self.App.Fixity.ProjectRepo.getSingleProject(project_name)

        result_of_all_file_confirmed = project_core.Run(True)

        if bool(result_of_all_file_confirmed['file_changed_found']):
            email_fixtures = EmailFixtures()
            self.App.Fixity.Configuration.setEmailConfiguration(email_fixtures.EmailInformation())
            flag = False

        update_project_algo = {}
        update_project_algo['selectedAlgo'] = algo_value_selected
        self.App.Fixity.Database.update(self.App.Fixity.Database._tableProject, update_project_algo, "id='" + str(project_core.getID()) + "'")
        project_core.setAlgorithm(algo_value_selected)
        result_of_all_file_confirmed_second = project_core.Run(True, False, True)

        try:
            self.project_fixtures.delete_testing_data()
        except:
            pass

        if bool(result_of_all_file_confirmed_second['file_changed_found']):
            flag = False

        print("---------------------------------------------------------------------\n")

        return [flag, ExpectedResults.ProjectTestCaseExpectedResult['change_algorithm'], FailedMessages.ProjectTestCaseFailMessages['change_algorithm']]

    def filters_files(self, selected_project):
        """
        Filters Files

        @param selected_project: project name to be filtered
        """

        print('Test Filters Project .........!')
        self.project_fixtures.load_verification_algorithm_data()

        self.project_fixtures.create_new_project(selected_project)

        project_core = self.App.Fixity.ProjectRepo.getSingleProject(selected_project)
        project_core.applyFilter('', self.project_fixtures.is_ignore_hidden_files)
        project_core.Run(False, False, False, 'test')

        project_core.applyFilter(self.project_fixtures.filters, self.project_fixtures.is_ignore_hidden_files)
        result_of_run_after_filter = project_core.Run(False, False, False, 'test')

        self.project_fixtures.load_verification_algorithm_data()

        confirmed = result_of_run_after_filter['confirmed']
        missing_file = result_of_run_after_filter['missing_file']
        created = result_of_run_after_filter['created']
        moved = result_of_run_after_filter['moved']
        corrupted_or_changed = result_of_run_after_filter['corrupted_or_changed']

        try:
            self.project_fixtures.delete_testing_data()
        except:
            pass

        print("---------------------------------------------------------------------\n")
        return [{0: confirmed, 1: missing_file, 2: created, 3: moved, 4: corrupted_or_changed}, ExpectedResults.ProjectTestCaseExpectedResult['filters_files'], FailedMessages.ProjectTestCaseFailMessages['filters_files']]

    def import_project(self, project_name):
        """
        Import Project

        @param project_name: project name to be import Project
        """
        print('Test Import Project .........!')
        self.project_fixtures.load_history_file()
        flag = True
        project_core = ProjectCore.ProjectCore()
        response = project_core.ImportProject(self.project_fixtures.test_history_file, project_name, True, False)
        project_core = self.App.Fixity.ProjectRepo.getSingleProject(project_name)

        if not response:
            return False

        try:
            project_core.getID()
            project_core.getTitle()
            flag = True
        except:
            flag = False
            pass

        try:
            self.project_fixtures.delete_testing_data()
        except:
            pass

        print("---------------------------------------------------------------------\n")
        return [flag, ExpectedResults.ProjectTestCaseExpectedResult['import_project'], FailedMessages.ProjectTestCaseFailMessages['run_project']]