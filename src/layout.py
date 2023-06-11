from dash import dcc, html
import dash_bootstrap_components as dbc

# Login layout
login_layout = html.Div([
    html.H2("Login"),
    html.Div([
        html.Label("Username:"),
        dcc.Input(id="login-username", type="text", placeholder="Enter your username"),
        html.Br(),
        html.Label("Password:"),
        dcc.Input(id="login-password", type="password", placeholder="Enter your password"),
        html.Br(),
        dbc.Button("Login", id="login-button", n_clicks=0),
        html.Br(),
        html.P("Don't have an account?"),
        html.A("Register Here", href="/register")
    ]),
    html.Div(id='login-output')
])


# Registration layout
registration_layout = html.Div([
    html.H2("Registration"),
    html.Div([
        html.Label("First Name:"),
        dcc.Input(id="register-firstname", type="text", placeholder="Enter your first name"),
        html.Br(),
        html.Label("Last Name:"),
        dcc.Input(id="register-lastname", type="text", placeholder="Enter your last name"),
        html.Br(),
        html.Label("Username:"),
        dcc.Input(id="register-username", type="text", placeholder="Enter a username"),
        html.Br(),
        html.Label("Password:"),
        dcc.Input(id="register-password", type="password", placeholder="Enter a password"),
        html.Br(),
        dbc.Button("Register", id="register-button", n_clicks=0),
        html.Br(),
        html.P("Already registered?"),
        html.A("Login Here", href="/login")
    ]),
    html.Div(id='registration-output')
])


# Main layout
main_layout = html.Div([
    html.Div(
        children=[
            html.Div(className='d-flex justify-content-end align-items-center', children=[
                dbc.Button('Admin', id='admin-button', className='btn-info', n_clicks=0, style={'display': 'none'}),
                dbc.Button('Account', id='account-button', className='btn-primary', n_clicks=0),
                dbc.Button('Logout', id='logout-button', className='btn-secondary', n_clicks=0)
            ])
        ]
    ),
    dcc.Dropdown(id='dummy-value', options=[1, 2], value=1, style={'display': 'none'}),
    html.H2(id='welcome-message-output'),
    html.H4("Select when you want to play"),
    html.Div([
        html.Label("Timeslots:"),
        dcc.Dropdown(id="timeslots", options=[], value=None, multi=True),
        dbc.Button("Register", id="register-timeslots-button", n_clicks=0)
    ], style={'width': '20%'}),
    html.Div(id='player-registration-output'),
    html.H4("Registrations"),
    html.Div([
        dcc.Tabs(id='timeslot-tabs', value='', children=[])
    ])
])


# Account layout
account_layout = html.Div([
    html.Div(
        children=[
            html.Div(className='d-flex justify-content-end align-items-center', children=[
                dbc.Button('Admin', id='admin-button', className='btn-info', n_clicks=0, style={'display': 'none'}),
                dbc.Button('Account', id='account-button', className='btn-primary', n_clicks=0),
                dbc.Button('Logout', id='logout-button', className='btn-secondary', n_clicks=0)
            ])
        ]
    ),
    dcc.Dropdown(id='dummy-value2', options=[1, 2], value=1, style={'display': 'none'}),
    html.H4("Select dates you want to cancel"),
    html.Div([
        html.Label("Timeslots:"),
        dcc.Dropdown(id="cancel-timeslots", options=[], value=None, multi=True),
        dbc.Button("Cancel", id="cancel-timeslots-button", n_clicks=0)
    ], style={'width': '20%'}),
    html.A("Return to overview", href="/main"),
    html.Div(id='player-cancel-output')
])

# Admin layout
admin_layout = html.Div([
    html.Div(
        children=[
            html.Div(className='d-flex justify-content-end align-items-center', children=[
                dbc.Button('Admin', id='admin-button', className='btn-info', n_clicks=0),
                dbc.Button('Account', id='account-button', className='btn-primary', n_clicks=0),
                dbc.Button('Logout', id='logout-button', className='btn-secondary', n_clicks=0)
            ])
        ]
    ),
    dcc.Dropdown(id='dummy-value3', options=[1, 2], value=1, style={'display': 'none'}),
    html.H4("User management"),
    html.Div([
        html.Label("Select a user:"),
        dcc.Dropdown(id="users-dropdown", options=[], value=None),
        dbc.Button("Promote to admin", id="promote-user-button", n_clicks=0),
        dbc.Button("Demote to normal", id="demote-user-button", n_clicks=0),
        dbc.Button("Delete user", id="delete-user-button", n_clicks=0),
    ], style={'width': '30%'}),
    html.A("Return to overview", href="/main"),
    html.Div(id='admin-output1'),
    html.Div(id='admin-output2'),
    html.Div(id='admin-output3')
])
