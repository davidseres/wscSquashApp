import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from flask import request, session, g
import psycopg2
from psycopg2 import errors
import datetime
from layout import registration_layout, main_layout, login_layout, account_layout, admin_layout
import db.users_db as users_db
import db.players_db as players_db
from db.connection import conn
from helpers import get_timeslots


# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY], suppress_callback_exceptions=True)
server = app.server
server.secret_key = '000'

# Estabilish connection to database
@app.server.before_request
def connect_db():
    # Create the 'users' and 'players' tables if they don't exist
    users_db.create_user_table(conn)
    players_db.create_players_table(conn)
    g.db = conn

# Define the layout of the app
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


# Display contents
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_content(pathname):
    if pathname == '/login':
        return login_layout
    elif pathname == '/register':
        return registration_layout
    elif pathname == '/account' and 'username' in session:
        return account_layout
    elif pathname == '/main' and 'username' in session:
        return main_layout
    elif pathname == '/admin' and 'username' in session and session['role'] == "admin":
        return admin_layout
    else:
        return login_layout

# Check login
@app.callback(
    Output('login-output', 'children'),
    Input('login-button', 'n_clicks'),
    [State('login-username', 'value'), State('login-password', 'value')]
)
def check_login(n_clicks, username, password):
    if n_clicks:
        if users_db.authenticate_user(g.db, username, password):
            [firstname, lastname, role] = users_db.get_first_and_last_names_and_role(conn, username)
            session['username'] = username
            session['firstname'] = firstname
            session['lastname'] = lastname
            session['role'] = role
            return dcc.Location(pathname='/main', id='login-success-url')
        else:
            return [dbc.Alert(
                "Invalid login credentials!", color="danger", dismissable=True, is_open=True, duration=4000
            )]
    else:
        return ""

# Page navigation
@app.callback(
    Output('url', 'pathname'),
    [Input('logout-button', 'n_clicks'), Input('account-button', 'n_clicks'), Input('admin-button', 'n_clicks')]
)
def logout(logout_click, account_click, admin_click):
    if logout_click:
        session.clear()
        return '/login'
    elif account_click:
        return '/account'
    elif admin_click:
        return '/admin'
    else:
        return '/main'


@app.callback(
    Output("registration-output", "children"),
    [Input("register-button", "n_clicks")],
    [State("register-username", "value"), State("register-password", "value"),
     State("register-firstname", "value"), State("register-lastname", "value")]
)
def register_new_user(n_clicks, username, password, firstname, lastname):
    if n_clicks:
        try:
            users_db.register_user(g.db, username, password, firstname, lastname)
            return [dbc.Alert(
                "Registration successful! You can now log in.", color="success",
                dismissable=True, is_open=True, duration=4000
            )]
        except psycopg2.errors.UniqueViolation:
            return dbc.Alert("Username is already taken. Please choose a different username.", color="danger",
                             dismissable=True, is_open=True, duration=4000)
    else:
        return ""


@app.callback(
    Output('welcome-message-output', 'children'),
    Input('dummy-value', 'value')
)
def welcome_message(value):
    return 'Welcome {} {}'.format(session['firstname'], session['lastname'])

# Fill dropdown with available options
@app.callback(
    Output('timeslots', 'options'),
    Input('dummy-value', 'value')
)
def update_timeslots(value):
    results = get_timeslots()

    # Get the timeslots already registered by the user
    registered_timeslots = players_db.get_player_registrations(g.db, session['username'])
    if registered_timeslots:
        registered_timeslots_map = [i.date() for i in list(zip(*registered_timeslots))[0]]

        # Disable the timeslots in the dropdown menu that the user has already registered for
        for item in results:
            if item['value'] in registered_timeslots_map:
                item['disabled'] = True
    else:
        for item in results:
            item['disabled'] = False

    return [{"label": item["label"], "value": item["value"], "disabled": item.get("disabled", False)} for item in results]

# Fill cancel dropdown on account page with available options
@app.callback(
    Output('cancel-timeslots', 'options'),
    Input('dummy-value2', 'value')
)
def update_cancel_timeslots(value):
    # Get the timeslots already registered by the user
    registered_timeslots = players_db.get_player_registrations(g.db, session['username'])
    registered_timeslots_map = [i.date() for i in list(zip(*registered_timeslots))[0]]

    return [{"label": item.strftime("%A %Y-%m-%d"), "value": item} for item in registered_timeslots_map]

# Register timeslots
@app.callback(
    Output("player-registration-output", "children"),
    [Input("register-timeslots-button", "n_clicks")],
    [State("timeslots", "value")]
)
def register_timeslots(n_clicks, timeslots):
    if n_clicks and timeslots is not None:
        for timeslot in timeslots:
            players_db.register_player(g.db, session['username'], timeslot)
        return dbc.Alert("Successful registration. Please refresh page to view table entry.", color="success",
                             dismissable=True, is_open=True, duration=4000)
    else:
        return ""

# Cancel timeslots
@app.callback(
    Output("player-cancel-output", "children"),
    [Input("cancel-timeslots-button", "n_clicks")],
    [State("cancel-timeslots", "value")]
)
def cancel_timeslots(n_clicks, timeslots_to_cancel):
    if n_clicks and timeslots_to_cancel is not None:
        for timeslot in timeslots_to_cancel:
            players_db.cancel_player_registrations(g.db, session['username'], timeslot)
        return dbc.Alert("Successful cancelation.", color="success",
                             dismissable=True, is_open=True, duration=4000)
    else:
        return ""


@app.callback(
    Output('timeslot-tabs', 'children'),
    Output('timeslot-tabs', 'value'),
    Input('dummy-value', 'value')
)
def update_timeslot_tabs(value):
    results = get_timeslots()  # Retrieve the next Tuesday and Thursday dates

    registrations = players_db.get_all_players_registrations(g.db)
    tabs = []

    for index, item in enumerate(results):
        timeslot = item['value']
        tab_label = item['label']

        timeslot_registrations = [(user, date, timeRegistration) for user, date, timeRegistration in registrations if
                                  date.date() == timeslot]

        # Create a table for the registrations
        if registrations:
            table = html.Table(
                [html.Tr([html.Th('No.'), html.Th('User'), html.Th('Date of registration')])] +  # Table headers
                [html.Tr([html.Td(i+1), html.Td(user), html.Td(timeRegistration)]) for i, (user, date, timeRegistration) in enumerate(timeslot_registrations) if date.date() == timeslot]
            )
        else:
            table = html.P("No players have registered for this timeslot.")

        # Create a tab for the timeslot with the registrations table
        tab = dcc.Tab(label=tab_label, value=timeslot, children=table)

        tabs.append(tab)

    return tabs, results[0]['value']

# ADMIN: Fill user dropdown on admin page with available options
@app.callback(
    Output('users-dropdown', 'options'),
    Input('dummy-value3', 'value')
)
def update_users_dropdown(value):
    # Get the timeslots already registered by the user
    all_users = users_db.get_all_users(g.db)

    return [{"label": f"{firstname} {lastname} - {username} ({role})", "value": username} for username, firstname, lastname, role in all_users]

# ADMIN: Promote user
@app.callback(
    Output("admin-output1", "children"),
    [Input("promote-user-button", "n_clicks")],
    [State("users-dropdown", "value")]
)
def promote_user(n_clicks, selected_user):
    if n_clicks and selected_user is not None:
        users_db.promote_user(g.db, selected_user)
        return dbc.Alert("User successfully promoted.", color="success",
                             dismissable=True, is_open=True, duration=4000)
    else:
        return ""

# ADMIN: Demote user
@app.callback(
    Output("admin-output2", "children"),
    [Input("demote-user-button", "n_clicks")],
    [State("users-dropdown", "value")]
)
def demote_user(n_clicks, selected_user):
    if n_clicks and selected_user is not None:
        users_db.demote_user(g.db, selected_user)
        return dbc.Alert("User successfully demoted.", color="success",
                             dismissable=True, is_open=True, duration=4000)
    else:
        return ""

# ADMIN: Delete user
@app.callback(
    Output("admin-output3", "children"),
    [Input("delete-user-button", "n_clicks")],
    [State("users-dropdown", "value")]
)
def delete_user(n_clicks, selected_user):
    if n_clicks and selected_user is not None:
        users_db.delete_user(g.db, selected_user)
        return dbc.Alert("User successfully deleted.", color="success",
                             dismissable=True, is_open=True, duration=4000)
    else:
        return ""

# ADMIN: show admin page button
@app.callback(
    Output('admin-button', 'style'),
    Input('dummy-value', 'value')
)
def show_admin_button(value):
    if session['role'] == 'admin':
        return {'display': 'block'}
    else:
        return {'display': 'none'}


if __name__ == "__main__":
    app.run_server(debug=True)
