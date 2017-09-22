import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckanext.dataviewanalytics.db import create_tables


class DataviewanalyticsPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IRoutes)

    create_tables()

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'dataviewanalytics')

    # IRoutes

    def before_map(self, m):
        '''Called before the routes map is generated
        '''

        # Register a new user
        m.connect('register', '/user/register', controller=
                  'ckanext.dataviewanalytics.controllers.ui_controller:DataViewAnalyticsUI',
                  action='register', conditions=dict(method=['GET', 'POST']))

        # Open a resource page
        m.connect('resource_read', '/dataset/{id}/resource/{resource_id}', controller=
                  'ckanext.dataviewanalytics.controllers.ui_controller:DataViewAnalyticsUI',
                  action='resource_read')

        # Edit a user
        m.connect('user_edit', '/user/edit/{id:.*}', controller=
                  'ckanext.dataviewanalytics.controllers.ui_controller:DataViewAnalyticsUI',
                  action='edit', ckan_icon='cog')

        # User dashboard
        m.connect('user_dashboard', '/dashboard', controller=
                  'ckanext.dataviewanalytics.controllers.ui_controller:DataViewAnalyticsUI',
                  action='dashboard', ckan_icon='list')

        return m

    def after_map(self, m):
        '''Called after routes map is set up
        '''
        return m
