<h1>Backtester Server</h1>
<hr>
<h2>Server Breakdown</h2>
<table>
    <tr>
        <th>Title</th>
        <th>HTML File</th>
        <th>Python Function</th>
        <th>Route</th>
        <th>Visibility</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>Home</td>
        <td>home.html</td>
        <td>home()</td>
        <td>/</td>
        <td>public</td>
        <td>Home page for landing HTTP requests.</td>
    </tr>
    <tr>
        <td>Login</td>
        <td>login.html</td>
        <td>login()</td>
        <td>/login</td>
        <td>public</td>
        <td>Login page for users.</td>
    </tr>
    <tr>
        <td>Registration</td>
        <td>registration.html</td>
        <td>registration()</td>
        <td>/registration</td>
        <td>public</td>
        <td>Account creation.</td>
    </tr>
    <tr>
        <td>Financial Strategy Dashboard</td>
        <td>dashboard.html</td>
        <td>dashboard()</td>
        <td>/dashboard</td>
        <td>private</td>
        <td>Page for viewing previously saved financial strategies and creating new strategies.</td>
    </tr>
    <tr>
        <td>View</td>
        <td>view.html</td>
        <td>view()</td>
        <td>/view</td>
        <td>private</td>
        <td>Viewing analysis results.</td>
    </tr>
    <tr>
        <td>Parameter View and Edit</td>
        <td>params.html</td>
        <td>params()</td>
        <td>/params</td>
        <td>private</td>
        <td>Viewing and editing parameters for saving previously saved strategies.</td>
    </tr>
</table>
<hr>
<h2>Database Structure</h2>
<strong>Volidity Database</strong>
<ol>
<li>data collection for storing financial data.</li>
    <ol>
        <li>id: unique identifier</li>
        <li>ticker: stock symbol</li>
        <li>data: pandas DF with stock data</li>
        <li>user: user to whom the data pertains</li>
    </ol>
<li>user collection for storing login/registration information</li>
    <ol>
        <li>id: unique identifier</li>
        <li>username: unique username for users to login</li>
        <li>password: password for unlocking user account</li>
        <li>name: name of user</li>
    </ol>
<li>strategy collection</li>
    <ol>
        <li>id: unique identifier</li>
        <li>ticker: stock symbol</li>
        <li>param1</li>
        <li>...</li>
        <li>paramn</li>
    </ol>
</ol>

Graphs:
1)  PnL vs Time (Date, X amount of labels), Linegraph
2)  Cumsum vs Time 
3)  Signals vs Time, Linegraph
4)  Histogram of daily % returns
5)  Time vs SD (if we have time), optional
