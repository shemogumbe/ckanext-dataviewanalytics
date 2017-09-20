import ckan.lib.base as base
import ckan.authz as authz
import ckan.model as model
import ckan.logic as logic
import ckan.logic.schema as schema
import ckan.lib.captcha as captcha
import ckan.lib.navl.dictization_functions as dictization_functions
import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as h
from ckan.common import config, c, request, response
from ckan.controllers.user import UserController
from ckan.controllers.package import PackageController
from ..db import UserAnalytics, DataAnalytics
from geoip import geolite2

render = base.render
NotFound = logic.NotFound
check_access = logic.check_access
NotAuthorized = logic.NotAuthorized
ValidationError = logic.ValidationError
DataError = dictization_functions.DataError
unflatten = dictization_functions.unflatten

'''List of all countries instrumental in converting
   country code to country name
'''
allCountries = [
  {"value": "AF", "text": "Afghanistan"},
  {"value": "AX", "text": "Aland Islands"},
  {"value": "AL", "text": "Albania"},
  {"value": "DZ", "text": "Algeria"},
  {"value": "AS", "text": "American Samoa"},
  {"value": "AD", "text": "Andorra"},
  {"value": "AO", "text": "Angola"},
  {"value": "AI", "text": "Anguilla"},
  {"value": "AQ", "text": "Antarctica"},
  {"value": "AG", "text": "Antigua and Barbuda"},
  {"value": "AR", "text": "Argentina"},
  {"value": "AM", "text": "Armenia"},
  {"value": "AW", "text": "Aruba"},
  {"value": "AU", "text": "Australia"},
  {"value": "AT", "text": "Austria"},
  {"value": "AZ", "text": "Azerbaijan"},
  {"value": "BS", "text": "Bahamas (the)"},
  {"value": "BH", "text": "Bahrain"},
  {"value": "BD", "text": "Bangladesh"},
  {"value": "BB", "text": "Barbados"},
  {"value": "BY", "text": "Belarus"},
  {"value": "BE", "text": "Belgium"},
  {"value": "BZ", "text": "Belize"},
  {"value": "BJ", "text": "Benin"},
  {"value": "BM", "text": "Bermuda"},
  {"value": "BT", "text": "Bhutan"},
  {"value": "BO", "text": "Bolivia (Plurinational State of)"},
  {"value": "BQ", "text": "Bonaire, Sint Eustatius and Saba"},
  {"value": "BA", "text": "Bosnia and Herzegovina"},
  {"value": "BW", "text": "Botswana"},
  {"value": "BV", "text": "Bouvet Island"},
  {"value": "BR", "text": "Brazil"},
  {"value": "IO", "text": "British Indian Ocean Territory (the)"},
  {"value": "BN", "text": "Brunei Darussalam"},
  {"value": "BG", "text": "Bulgaria"},
  {"value": "BF", "text": "Burkina Faso"},
  {"value": "BI", "text": "Burundi"},
  {"value": "CV", "text": "Cabo Verde"},
  {"value": "KH", "text": "Cambodia"},
  {"value": "CM", "text": "Cameroon"},
  {"value": "CA", "text": "Canada"},
  {"value": "KY", "text": "Cayman Islands (the)"},
  {"value": "CF", "text": "Central African Republic (the)"},
  {"value": "TD", "text": "Chad"},
  {"value": "CL", "text": "Chile"},
  {"value": "CN", "text": "China"},
  {"value": "CX", "text": "Christmas Island"},
  {"value": "CC", "text": "Cocos (Keeling) Islands (the)"},
  {"value": "CO", "text": "Colombia"},
  {"value": "KM", "text": "Comoros (the)"},
  {"value": "CD", "text": "Congo (the Democratic Republic of the)"},
  {"value": "CG", "text": "Congo (the)"},
  {"value": "CK", "text": "Cook Islands (the)"},
  {"value": "CR", "text": "Costa Rica"},
  {"value": "CI", "text": "Cote d'Ivoire"},
  {"value": "HR", "text": "Croatia"},
  {"value": "CU", "text": "Cuba"},
  {"value": "CW", "text": "Curacao"},
  {"value": "CY", "text": "Cyprus"},
  {"value": "CZ", "text": "Czechia"},
  {"value": "DK", "text": "Denmark"},
  {"value": "DJ", "text": "Djibouti"},
  {"value": "DM", "text": "Dominica"},
  {"value": "DO", "text": "Dominican Republic (the)"},
  {"value": "EC", "text": "Ecuador"},
  {"value": "EG", "text": "Egypt"},
  {"value": "SV", "text": "El Salvador"},
  {"value": "GQ", "text": "Equatorial Guinea"},
  {"value": "ER", "text": "Eritrea"},
  {"value": "EE", "text": "Estonia"},
  {"value": "ET", "text": "Ethiopia"},
  {"value": "FK", "text": "Falkland Islands (the) [Malvinas]"},
  {"value": "FO", "text": "Faroe Islands (the)"},
  {"value": "FJ", "text": "Fiji"},
  {"value": "FI", "text": "Finland"},
  {"value": "FR", "text": "France"},
  {"value": "GF", "text": "French Guiana"},
  {"value": "PF", "text": "French Polynesia"},
  {"value": "TF", "text": "French Southern Territories (the)"},
  {"value": "GA", "text": "Gabon"},
  {"value": "GM", "text": "Gambia (the)"},
  {"value": "GE", "text": "Georgia"},
  {"value": "DE", "text": "Germany"},
  {"value": "GH", "text": "Ghana"},
  {"value": "GI", "text": "Gibraltar"},
  {"value": "GR", "text": "Greece"},
  {"value": "GL", "text": "Greenland"},
  {"value": "GD", "text": "Grenada"},
  {"value": "GP", "text": "Guadeloupe"},
  {"value": "GU", "text": "Guam"},
  {"value": "GT", "text": "Guatemala"},
  {"value": "GG", "text": "Guernsey"},
  {"value": "GN", "text": "Guinea"},
  {"value": "GW", "text": "Guinea-Bissau"},
  {"value": "GY", "text": "Guyana"},
  {"value": "HT", "text": "Haiti"},
  {"value": "HM", "text": "Heard Island and McDonald Islands"},
  {"value": "VA", "text": "Holy See (the)"},
  {"value": "HN", "text": "Honduras"},
  {"value": "HK", "text": "Hong Kong"},
  {"value": "HU", "text": "Hungary"},
  {"value": "IS", "text": "Iceland"},
  {"value": "IN", "text": "India"},
  {"value": "ID", "text": "Indonesia"},
  {"value": "IR", "text": "Iran (Islamic Republic of)"},
  {"value": "IQ", "text": "Iraq"},
  {"value": "IE", "text": "Ireland"},
  {"value": "IM", "text": "Isle of Man"},
  {"value": "IL", "text": "Israel"},
  {"value": "IT", "text": "Italy"},
  {"value": "JM", "text": "Jamaica"},
  {"value": "JP", "text": "Japan"},
  {"value": "JE", "text": "Jersey"},
  {"value": "JO", "text": "Jordan"},
  {"value": "KZ", "text": "Kazakhstan"},
  {"value": "KE", "text": "Kenya"},
  {"value": "KI", "text": "Kiribati"},
  {"value": "KP", "text": "Korea (the Democratic People's Republic of)"},
  {"value": "KR", "text": "Korea (the Republic of)"},
  {"value": "KW", "text": "Kuwait"},
  {"value": "KG", "text": "Kyrgyzstan"},
  {"value": "LA", "text": "Lao People's Democratic Republic (the)"},
  {"value": "LV", "text": "Latvia"},
  {"value": "LB", "text": "Lebanon"},
  {"value": "LS", "text": "Lesotho"},
  {"value": "LR", "text": "Liberia"},
  {"value": "LY", "text": "Libya"},
  {"value": "LI", "text": "Liechtenstein"},
  {"value": "LT", "text": "Lithuania"},
  {"value": "LU", "text": "Luxembourg"},
  {"value": "MO", "text": "Macao"},
  {"value": "MK", "text": "Macedonia (the former Yugoslav Republic of)"},
  {"value": "MG", "text": "Madagascar"},
  {"value": "MW", "text": "Malawi"},
  {"value": "MY", "text": "Malaysia"},
  {"value": "MV", "text": "Maldives"},
  {"value": "ML", "text": "Mali"},
  {"value": "MT", "text": "Malta"},
  {"value": "MH", "text": "Marshall Islands (the)"},
  {"value": "MQ", "text": "Martinique"},
  {"value": "MR", "text": "Mauritania"},
  {"value": "MU", "text": "Mauritius"},
  {"value": "YT", "text": "Mayotte"},
  {"value": "MX", "text": "Mexico"},
  {"value": "FM", "text": "Micronesia (Federated States of)"},
  {"value": "MD", "text": "Moldova (the Republic of)"},
  {"value": "MC", "text": "Monaco"},
  {"value": "MN", "text": "Mongolia"},
  {"value": "ME", "text": "Montenegro"},
  {"value": "MS", "text": "Montserrat"},
  {"value": "MA", "text": "Morocco"},
  {"value": "MZ", "text": "Mozambique"},
  {"value": "MM", "text": "Myanmar"},
  {"value": "NA", "text": "Namibia"},
  {"value": "NR", "text": "Nauru"},
  {"value": "NP", "text": "Nepal"},
  {"value": "NL", "text": "Netherlands (the)"},
  {"value": "NC", "text": "New Caledonia"},
  {"value": "NZ", "text": "New Zealand"},
  {"value": "NI", "text": "Nicaragua"},
  {"value": "NE", "text": "Niger (the)"},
  {"value": "NG", "text": "Nigeria"},
  {"value": "NU", "text": "Niue"},
  {"value": "NF", "text": "Norfolk Island"},
  {"value": "MP", "text": "Northern Mariana Islands (the)"},
  {"value": "NO", "text": "Norway"},
  {"value": "OM", "text": "Oman"},
  {"value": "PK", "text": "Pakistan"},
  {"value": "PW", "text": "Palau"},
  {"value": "PS", "text": "Palestine, State of"},
  {"value": "PA", "text": "Panama"},
  {"value": "PG", "text": "Papua New Guinea"},
  {"value": "PY", "text": "Paraguay"},
  {"value": "PE", "text": "Peru"},
  {"value": "PH", "text": "Philippines (the)"},
  {"value": "PN", "text": "Pitcairn"},
  {"value": "PL", "text": "Poland"},
  {"value": "PT", "text": "Portugal"},
  {"value": "PR", "text": "Puerto Rico"},
  {"value": "QA", "text": "Qatar"},
  {"value": "RE", "text": "Reunion"},
  {"value": "RO", "text": "Romania"},
  {"value": "RU", "text": "Russian Federation (the)"},
  {"value": "RW", "text": "Rwanda"},
  {"value": "BL", "text": "Saint Barthelemy"},
  {"value": "SH", "text": "Saint Helena, Ascension and Tristan da Cunha"},
  {"value": "KN", "text": "Saint Kitts and Nevis"},
  {"value": "LC", "text": "Saint Lucia"},
  {"value": "MF", "text": "Saint Martin (French part)"},
  {"value": "PM", "text": "Saint Pierre and Miquelon"},
  {"value": "VC", "text": "Saint Vincent and the Grenadines"},
  {"value": "WS", "text": "Samoa"},
  {"value": "SM", "text": "San Marino"},
  {"value": "ST", "text": "Sao Tome and Principe"},
  {"value": "SA", "text": "Saudi Arabia"},
  {"value": "SN", "text": "Senegal"},
  {"value": "RS", "text": "Serbia"},
  {"value": "SC", "text": "Seychelles"},
  {"value": "SL", "text": "Sierra Leone"},
  {"value": "SG", "text": "Singapore"},
  {"value": "SX", "text": "Sint Maarten (Dutch part)"},
  {"value": "SK", "text": "Slovakia"},
  {"value": "SI", "text": "Slovenia"},
  {"value": "SB", "text": "Solomon Islands"},
  {"value": "SO", "text": "Somalia"},
  {"value": "ZA", "text": "South Africa"},
  {"value": "GS", "text": "South Georgia and the South Sandwich Islands"},
  {"value": "SS", "text": "South Sudan"},
  {"value": "ES", "text": "Spain"},
  {"value": "LK", "text": "Sri Lanka"},
  {"value": "SD", "text": "Sudan (the)"},
  {"value": "SR", "text": "Suriname"},
  {"value": "SJ", "text": "Svalbard and Jan Mayen"},
  {"value": "SZ", "text": "Swaziland"},
  {"value": "SE", "text": "Sweden"},
  {"value": "CH", "text": "Switzerland"},
  {"value": "SY", "text": "Syrian Arab Republic"},
  {"value": "TW", "text": "Taiwan (Province of China)"},
  {"value": "TJ", "text": "Tajikistan"},
  {"value": "TZ", "text": "Tanzania, United Republic of"},
  {"value": "TH", "text": "Thailand"},
  {"value": "TL", "text": "Timor-Leste"},
  {"value": "TG", "text": "Togo"},
  {"value": "TK", "text": "Tokelau"},
  {"value": "TO", "text": "Tonga"},
  {"value": "TT", "text": "Trinidad and Tobago"},
  {"value": "TN", "text": "Tunisia"},
  {"value": "TR", "text": "Turkey"},
  {"value": "TM", "text": "Turkmenistan"},
  {"value": "TC", "text": "Turks and Caicos Islands (the)"},
  {"value": "TV", "text": "Tuvalu"},
  {"value": "UG", "text": "Uganda"},
  {"value": "UA", "text": "Ukraine"},
  {"value": "AE", "text": "United Arab Emirates (the)"},
  {"value": "GB", "text": "United Kingdom of Great Britain and Northern Ireland (the)"},
  {"value": "UM", "text": "United States Minor Outlying Islands (the)"},
  {"value": "US", "text": "United States of America (the)"},
  {"value": "UY", "text": "Uruguay"},
  {"value": "UZ", "text": "Uzbekistan"},
  {"value": "VU", "text": "Vanuatu"},
  {"value": "VE", "text": "Venezuela (Bolivarian Republic of)"},
  {"value": "VN", "text": "Viet Nam"},
  {"value": "VG", "text": "Virgin Islands (British)"},
  {"value": "VI", "text": "Virgin Islands (U.S.)"},
  {"value": "WF", "text": "Wallis and Futuna"},
  {"value": "EH", "text": "Western Sahara*"},
  {"value": "YE", "text": "Yemen"},
  {"value": "ZM", "text": "Zambia"},
  {"value": "ZW", "text": "Zimbabwe"}
]

'''List of available occupations to select from
   during user registration
'''
occupations = [
    'Student',
    'Journalist',
    'Researcher',
    'Programmer',
    'Civil servant',
    'Entrepreneur',
    'Data scientist'
]

def set_repoze_user(user_id):
    '''Set the repoze.who cookie to match a given user_id'''
    if 'repoze.who.plugins' in request.environ:
        rememberer = request.environ['repoze.who.plugins']['friendlyform']
        identity = {'repoze.who.userid': user_id}
        response.headerlist += rememberer.remember(request.environ,
                                                   identity)

def use_country_name(country_code):
    '''Returns a country name when passed a country code
    '''
    for country in allCountries:
        if country['value'] == country_code:
            return country['text']

def save_user_extras(data, user, context):
    '''Save extra user attributes to database
    '''
    session = context['session']

    user_extras = UserAnalytics(
        user_id=user['id'],
        country=use_country_name(data['country']),
        occupation=data['occupation']
    )
    
    session.add(user_extras)
    session.commit()

def has_user_visited_data(user_id, resource_id, context):
    '''Checks if the user has visited the resource
    '''
    session = context['session']
    data_details = session.query(DataAnalytics).filter_by(user_id=user_id).all()
    resources_visited = [data.resource_id for data in data_details if data.resource_id == resource_id]
    return resources_visited

def save_view_details(viewer_id, resource_id, context):
    '''Save the viewer attributes to database
    '''
    if not has_user_visited_data(viewer_id, resource_id, context):
        session = context['session']
        
        user_details = session.query(UserAnalytics).filter_by(user_id=viewer_id).first()
        country = user_details.country
        occupation = user_details.occupation

        view_details = DataAnalytics(
            resource_id=resource_id,
            user_id=viewer_id,
            country=country,
            occupation=occupation
        )

        session.add(view_details)
        session.commit()


class DataViewAnalyticsUI(UserController, PackageController):
    
    def new(self, data=None, errors=None, error_summary=None):

        '''GET to display a form for registering a new user.
            or POST the form data to actually do the user registration.
        '''
        context = { 'model': model,
                    'session': model.Session,
                    'user': c.user,
                    'auth_user_obj': c.userobj,
                    'schema': self._new_form_to_db_schema(),
                    'save': 'save' in request.params}

        try:
            check_access('user_create', context)
        except NotAuthorized:
            abort(403, _('Unauthorized to create a user'))

        if context['save'] and not data:
            return self._save_new(context)

        if c.user and not data and not authz.is_sysadmin(c.user):
            # #1799 Don't offer the registration form if already logged in
            return render('user/logout_first.html')
        match = geolite2.lookup_mine()
        origin = match.country
        data = data or {}
        errors = errors or {}
        error_summary = error_summary or {}
        vars = {'data': data, 'errors': errors, 'error_summary': error_summary, 'origin': origin,
        'countries': allCountries, 'occupations': occupations}
        c.is_sysadmin = authz.is_sysadmin(c.user)
        c.form = render(self.new_user_form, extra_vars=vars)
        return render('user/new.html')

    def _save_new(self, context):
        try:
            data_dict = logic.clean_dict(unflatten(
                logic.tuplize_dict(logic.parse_params(request.params))))
            context['message'] = data_dict.get('log_message', '')
            captcha.check_recaptcha(request)
            user = toolkit.get_action('user_create')(context, data_dict)
        except NotAuthorized:
            abort(403, _('Unauthorized to create user %s') % '')
        except NotFound, e:
            abort(404, _('User not found'))
        except DataError:
            abort(400, _(u'Integrity Error'))
        except captcha.CaptchaError:
            error_msg = _(u'Bad Captcha. Please try again.')
            h.flash_error(error_msg)
            return self.new(data_dict)
        except ValidationError, e:
            errors = e.error_dict
            error_summary = e.error_summary
            return self.new(data_dict, errors, error_summary)
        if not c.user:
            '''Save extra user registration details at this point
            '''
            save_user_extras(data_dict, user, context)
            # log the user in programatically
            set_repoze_user(data_dict['name'])
            h.redirect_to(controller='user', action='me', __ckan_no_root=True)
        else:
            # #1799 User has managed to register whilst logged in - warn user
            # they are not re-logged in as new user.
            h.flash_success(_('User "%s" is now registered but you are still '
                            'logged in as "%s" from before') %
                            (data_dict['name'], c.user))
            if authz.is_sysadmin(c.user):
                # the sysadmin created a new user. We redirect him to the
                # activity page for the newly created user
                h.redirect_to(controller='user',
                              action='activity',
                              id=data_dict['name'])
            else:
                return render('user/logout_first.html')

    def resource_read(self, id, resource_id):
        context = {'model': model, 'session': model.Session,
                   'user': c.user,
                   'auth_user_obj': c.userobj,
                   'for_view': True}
        if context['user']:
            '''If user is logged in
            '''
            viewer_id = context['auth_user_obj'].id
            save_view_details(viewer_id, resource_id, context)
        try:
            c.package = toolkit.get_action('package_show')(context, {'id': id})
        except (NotFound, NotAuthorized):
            abort(404, _('Dataset not found'))

        for resource in c.package.get('resources', []):
            if resource['id'] == resource_id:
                c.resource = resource
                break
        if not c.resource:
            abort(404, _('Resource not found'))

        # required for nav menu
        c.pkg = context['package']
        c.pkg_dict = c.package
        dataset_type = c.pkg.type or 'dataset'

        # get package license info
        license_id = c.package.get('license_id')
        try:
            c.package['isopen'] = model.Package.\
                get_license_register()[license_id].isopen()
        except KeyError:
            c.package['isopen'] = False

        # TODO: find a nicer way of doing this
        c.datastore_api = '%s/api/action' % \
            config.get('ckan.site_url', '').rstrip('/')

        c.resource['can_be_previewed'] = self._resource_preview(
            {'resource': c.resource, 'package': c.package})

        resource_views = toolkit.get_action('resource_view_list')(
            context, {'id': resource_id})
        c.resource['has_views'] = len(resource_views) > 0

        current_resource_view = None
        view_id = request.GET.get('view_id')
        if c.resource['can_be_previewed'] and not view_id:
            current_resource_view = None
        elif c.resource['has_views']:
            if view_id:
                current_resource_view = [rv for rv in resource_views
                                         if rv['id'] == view_id]
                if len(current_resource_view) == 1:
                    current_resource_view = current_resource_view[0]
                else:
                    abort(404, _('Resource view not found'))
            else:
                current_resource_view = resource_views[0]

        vars = {'resource_views': resource_views,
                'current_resource_view': current_resource_view,
                'dataset_type': dataset_type}

        template = self._resource_template(dataset_type)
        return render(template, extra_vars=vars)