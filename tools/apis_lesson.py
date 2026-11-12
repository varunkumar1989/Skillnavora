"""Lesson: APIs for Product Managers (a separate lesson page on the site). Plain language, worked example, practice."""

def _pre(code):
    return f'<pre style="background:#0f1020;color:#e8e8f0;padding:14px 16px;border-radius:10px;overflow-x:auto;font-size:14px;line-height:1.55;max-width:100%">{code}</pre>'

def body():
    return f"""<section style="padding-top:28px"><div class="wrap" style="max-width:860px">

<div class="card" style="border:2px solid #6C4CF5;padding:18px 20px;margin:0 0 24px">
<b>How to use this lesson.</b> Read each part, look at the worked example, then do the practice at the end. You don't need to code. The aim is to be able to read an API request, explain it to an engineer, and spot what is wrong when something breaks.
</div>

<h2 class="sec-h">1. What an API is</h2>
<p class="sub">An API (Application Programming Interface) is a set of rules that lets one program ask another for something. Apps rarely hold their own business data. They ask a server, and the server answers.</p>
<p>Think of a restaurant. You are the <b>user</b>, the waiter is the <b>API</b>, and the kitchen is the <b>backend</b>. You never go into the kitchen, and the waiter takes your order in a fixed format.</p>
<p>Every API call has two halves:</p>
<ul>
<li><b>Request</b> (from the app): a method (what to do), an endpoint (the address to act on), headers (extra details such as the login), and often a body (the data, usually in JSON).</li>
<li><b>Response</b> (from the server): a status code (the outcome), and often a body (the result).</li>
</ul>

<h2 class="sec-h" style="margin-top:34px">2. Worked example: placing an order</h2>
<p class="sub">The user taps <b>Place order</b>. Here is what happens behind the screen.</p>
<ol>
<li><b>The app builds the request.</b>{_pre('POST /orders<br>Content-Type: application/json<br>Authorization: Bearer &lt;login token&gt;<br><br>{<br>  "customerId": 123,<br>  "productId": 456,<br>  "quantity": 2,<br>  "amount": 1500<br>}')}</li>
<li><b>The API checks it first.</b> Is the user logged in (otherwise <code>401</code>)? Is the JSON valid with every required field (otherwise <code>400</code>)? Does the product exist (otherwise <code>404</code>)?</li>
<li><b>The backend does the work:</b> it creates the order, reserves stock and calls the payment step.</li>
<li><b>The API replies</b> <code>201 Created</code> with the new order: ID 789, status Confirmed. The app shows "Order placed".</li>
</ol>

<h3 style="margin-top:22px">What the API needs before it will accept a request</h3>
<ul>
<li>The exact endpoint and method (<code>POST /orders</code>)</li>
<li>Required fields with the right types. <code>customerId</code> must be a number, not <code>"123"</code>, if the API says so.</li>
<li>Authentication: usually a login token or an API key</li>
<li>The <code>Content-Type: application/json</code> header</li>
<li>Documentation of all of the above, often an OpenAPI (Swagger) specification</li>
</ul>

<h3 style="margin-top:22px">How payment usually works</h3>
<p>The example above shows the order and its result, not every payment step. The usual pattern is:</p>
<ol>
<li>The order is created first, usually as <code>pending_payment</code>.</li>
<li>The backend sends the charge to a payment provider. Card details go to the provider directly, which keeps most card data out of your own systems.</li>
<li>The provider approves or declines, and returns the result.</li>
<li>On success the order becomes <code>Confirmed</code>. Some designs finish inside one request, as in the example. Others return <code>pending</code> and send a later notification, called a webhook.</li>
</ol>

<div class="card" style="border-left:4px solid #6C4CF5;padding:14px 16px;margin:18px 0">
<b>Questions a product manager should ask</b>
<ul style="margin:8px 0 0">
<li>Is <code>amount</code> in rupees or paise? Write it in the specification.</li>
<li>Does the server recalculate the price from the product and quantity? It should. If it trusts the <code>amount</code> the app sends, a user could change the price.</li>
<li>If payment is declined after the order exists, is the order cancelled or left pending?</li>
</ul>
</div>

<h2 class="sec-h" style="margin-top:34px">3. HTTP methods: what each one means</h2>
<p class="sub">A method says what to do with the thing named in the endpoint. Two properties matter for product work. <b>Safe</b> means the call changes nothing. <b>Idempotent</b> means that repeating the same call leaves the same result, which matters when a network error hides the answer and the app retries.</p>
<div style="overflow-x:auto"><table class="ap-t" style="width:100%;border-collapse:collapse;font-size:15px;min-width:520px">
<tr><th style="text-align:left;padding:8px;border-bottom:1px solid #ddd">Method</th><th style="text-align:left;padding:8px;border-bottom:1px solid #ddd">Purpose</th><th style="text-align:left;padding:8px;border-bottom:1px solid #ddd">Example</th><th style="text-align:left;padding:8px;border-bottom:1px solid #ddd">Safe</th><th style="text-align:left;padding:8px;border-bottom:1px solid #ddd">Idempotent</th></tr>
<tr><td style="padding:8px"><code>GET</code></td><td style="padding:8px">Read data</td><td style="padding:8px"><code>/customers/123</code></td><td style="padding:8px">Yes</td><td style="padding:8px">Yes</td></tr>
<tr><td style="padding:8px"><code>POST</code></td><td style="padding:8px">Create or start something</td><td style="padding:8px"><code>/orders</code></td><td style="padding:8px">No</td><td style="padding:8px">No</td></tr>
<tr><td style="padding:8px"><code>PUT</code></td><td style="padding:8px">Replace the whole record</td><td style="padding:8px"><code>/customers/123</code></td><td style="padding:8px">No</td><td style="padding:8px">Yes</td></tr>
<tr><td style="padding:8px"><code>PATCH</code></td><td style="padding:8px">Change selected fields</td><td style="padding:8px"><code>/customers/123</code></td><td style="padding:8px">No</td><td style="padding:8px">Not guaranteed</td></tr>
<tr><td style="padding:8px"><code>DELETE</code></td><td style="padding:8px">Remove a record</td><td style="padding:8px"><code>/addresses/123</code></td><td style="padding:8px">No</td><td style="padding:8px">Yes</td></tr>
</table></div>

<div class="card" style="margin:16px 0"><b>GET</b> asks for a record and changes nothing, so it has no body. Success returns <code>200 OK</code> with the customer as JSON. A missing customer returns <code>404 Not Found</code>. <i>Product takeaway:</i> GET is safe to repeat, so it can be cached.</div>
<div class="card" style="margin:16px 0"><b>POST</b> creates a new record or starts an operation, and usually returns <code>201 Created</code>. <i>Product takeaway:</i> repeating a POST can create duplicates unless the API supports idempotency keys, a unique ID sent with each attempt.</div>
<div class="card" style="margin:16px 0"><b>PUT</b> sends the complete record and replaces the stored one. If you leave out a field such as <code>city</code>, PUT can clear it. <i>Product takeaway:</i> PUT means a full update; use PATCH to change one field.</div>
<div class="card" style="margin:16px 0"><b>PATCH</b> sends only the fields that change, for example <code>{{"phone": "9876543210"}}</code>. <i>Product takeaway:</i> use PATCH for a single setting such as a notification preference.</div>
<div class="card" style="margin:16px 0"><b>DELETE</b> removes a record and returns <code>204 No Content</code> (or <code>200</code>, or <code>404</code> if it is already gone). <i>Product takeaway:</i> check whether deletion is permanent or soft, and any audit or legal rules, before you specify it.</div>

<h2 class="sec-h" style="margin-top:34px">4. Status codes: reading the first digit</h2>
<p class="sub">The first digit tells you who has to act.</p>
<div style="overflow-x:auto"><table style="width:100%;border-collapse:collapse;font-size:15px;min-width:520px">
<tr><th style="text-align:left;padding:8px;border-bottom:1px solid #ddd">Range</th><th style="text-align:left;padding:8px;border-bottom:1px solid #ddd">Meaning</th><th style="text-align:left;padding:8px;border-bottom:1px solid #ddd">Who acts</th></tr>
<tr><td style="padding:8px"><b>1xx</b></td><td style="padding:8px">Informational: still in progress</td><td style="padding:8px">Rarely visible</td></tr>
<tr><td style="padding:8px"><b>2xx</b></td><td style="padding:8px">Success</td><td style="padding:8px">Nobody</td></tr>
<tr><td style="padding:8px"><b>3xx</b></td><td style="padding:8px">Redirect: a new address to follow</td><td style="padding:8px">The app</td></tr>
<tr><td style="padding:8px"><b>4xx</b></td><td style="padding:8px">Client error: the request or the access was wrong</td><td style="padding:8px">The UI or the data</td></tr>
<tr><td style="padding:8px"><b>5xx</b></td><td style="padding:8px">Server error: the server failed</td><td style="padding:8px">Engineering</td></tr>
</table></div>
<p style="margin-top:14px">Common codes:</p>
<div style="overflow-x:auto"><table style="width:100%;border-collapse:collapse;font-size:15px;min-width:520px">
<tr><th style="text-align:left;padding:8px;border-bottom:1px solid #ddd">Code</th><th style="text-align:left;padding:8px;border-bottom:1px solid #ddd">Name</th><th style="text-align:left;padding:8px;border-bottom:1px solid #ddd">What it means for the product</th></tr>
<tr><td style="padding:8px"><code>200</code></td><td style="padding:8px">OK</td><td style="padding:8px">Customer details returned</td></tr>
<tr><td style="padding:8px"><code>201</code></td><td style="padding:8px">Created</td><td style="padding:8px">New order created</td></tr>
<tr><td style="padding:8px"><code>204</code></td><td style="padding:8px">No Content</td><td style="padding:8px">Deleted, nothing returned</td></tr>
<tr><td style="padding:8px"><code>301</code></td><td style="padding:8px">Moved Permanently</td><td style="padding:8px">The record has a new address</td></tr>
<tr><td style="padding:8px"><code>304</code></td><td style="padding:8px">Not Modified</td><td style="padding:8px">Use the copy you already have</td></tr>
<tr><td style="padding:8px"><code>400</code></td><td style="padding:8px">Bad Request</td><td style="padding:8px">The data sent was invalid</td></tr>
<tr><td style="padding:8px"><code>401</code></td><td style="padding:8px">Unauthorized</td><td style="padding:8px">Not logged in, or the login has expired</td></tr>
<tr><td style="padding:8px"><code>403</code></td><td style="padding:8px">Forbidden</td><td style="padding:8px">Logged in, but not allowed to do this</td></tr>
<tr><td style="padding:8px"><code>404</code></td><td style="padding:8px">Not Found</td><td style="padding:8px">The order or record does not exist</td></tr>
<tr><td style="padding:8px"><code>409</code></td><td style="padding:8px">Conflict</td><td style="padding:8px">Clashes with existing data, such as a duplicate</td></tr>
<tr><td style="padding:8px"><code>429</code></td><td style="padding:8px">Too Many Requests</td><td style="padding:8px">Rate limit reached: retry later</td></tr>
<tr><td style="padding:8px"><code>500</code></td><td style="padding:8px">Internal Server Error</td><td style="padding:8px">Unexpected failure on the server</td></tr>
<tr><td style="padding:8px"><code>503</code></td><td style="padding:8px">Service Unavailable</td><td style="padding:8px">Service down or overloaded</td></tr>
<tr><td style="padding:8px"><code>504</code></td><td style="padding:8px">Gateway Timeout</td><td style="padding:8px">Another service did not answer in time</td></tr>
</table></div>
<div class="card" style="border-left:4px solid #6C4CF5;padding:14px 16px;margin:18px 0"><b>When you report a bug,</b> include the status code and the time it happened. A 4xx points at the screen or the data. A 5xx points at engineering.</div>

<h2 class="sec-h" style="margin-top:34px">5. Endpoints: the address structure</h2>
<p class="sub">An endpoint is the specific address that performs an action. Each part has a job:</p>
{_pre('https://api.shop.com  /v1  /customers  /123  /orders  ?status=paid&amp;limit=10')}
<ul>
<li><b>Base address:</b> where the API lives.</li>
<li><b>/v1:</b> the version. It lets the API change without breaking older apps.</li>
<li><b>/customers:</b> the resource, written as a plural noun.</li>
<li><b>/123:</b> which one. This is a path parameter.</li>
<li><b>/orders:</b> a related resource under that customer.</li>
<li><b>?status=paid&amp;limit=10:</b> query parameters, covered in the next part.</li>
</ul>
<p><b>Design rules:</b> use nouns, not actions (<code>/orders</code>, not <code>/createOrder</code>), keep collection names plural, and let the method carry the action.</p>

<h2 class="sec-h" style="margin-top:34px">6. Parameters: where the information goes</h2>
<p class="sub">A parameter is a piece of information the request passes to the API. Each kind of parameter has its own place in the request, and each answers a different question.</p>
<div style="overflow-x:auto"><table style="width:100%;border-collapse:collapse;font-size:15px;min-width:520px">
<tr><th style="text-align:left;padding:8px;border-bottom:1px solid #ddd">Kind</th><th style="text-align:left;padding:8px;border-bottom:1px solid #ddd">Where it sits</th><th style="text-align:left;padding:8px;border-bottom:1px solid #ddd">Question it answers</th><th style="text-align:left;padding:8px;border-bottom:1px solid #ddd">Example</th></tr>
<tr><td style="padding:8px"><b>Path</b></td><td style="padding:8px">In the URL path, between slashes</td><td style="padding:8px">Which specific record?</td><td style="padding:8px"><code>/orders/123</code></td></tr>
<tr><td style="padding:8px"><b>Query</b></td><td style="padding:8px">After the <code>?</code></td><td style="padding:8px">How should the results be filtered, sorted or paged?</td><td style="padding:8px"><code>?status=shipped</code></td></tr>
<tr><td style="padding:8px"><b>Header</b></td><td style="padding:8px">In the request headers</td><td style="padding:8px">Who is asking, and in what format?</td><td style="padding:8px"><code>Authorization: Bearer …</code></td></tr>
<tr><td style="padding:8px"><b>Body</b></td><td style="padding:8px">In the JSON body</td><td style="padding:8px">What data should be created or changed?</td><td style="padding:8px"><code>{{"quantity": 2}}</code></td></tr>
</table></div>

<h3 style="margin-top:26px">Path parameters identify one record</h3>
<p>A path parameter is a value inside the URL path that points at one resource. Read the request from left to right:</p>
{_pre('GET /orders/123')}
<div class="card" style="margin:14px 0;padding:14px 16px">
<ul style="margin:0">
<li><b>GET</b> is the action: read.</li>
<li><b>/orders</b> identifies the resource type: the collection of orders.</li>
<li><b>123</b> identifies the specific order: the path parameter.</li>
</ul>
</div>
<p>The same pattern works for other resources:</p>
<ul>
<li><code>GET /customers/456</code>: one customer</li>
<li><code>GET /products/789</code>: one product</li>
<li><code>GET /shipments/12345</code>: one shipment, so you can check its status</li>
</ul>

<h3 style="margin-top:22px">Business use cases</h3>
<ul>
<li>Retrieve a customer's profile</li>
<li>View a specific order</li>
<li>Check the status of a shipment</li>
<li>Retrieve a particular product</li>
</ul>

<h3 style="margin-top:22px">Common mistakes with path parameters</h3>
<ul>
<li><b>Wrong or missing ID.</b> The API returns <code>404 Not Found</code>. Check that the app passes the right ID, for example a shipment number instead of an order number.</li>
<li><b>Changing the type.</b> If the API expects a number, <code>/orders/abc</code> will fail. Check the documentation for each ID type.</li>
<li><b>Guessable IDs without access checks.</b> If the ID is simply 1, 2, 3, a user can try other numbers and read someone else's order. The server must check that the logged-in user is allowed to see the record, even when the ID is valid. This is a common security bug, and the answer is an access check on every request.</li>
</ul>

<div class="card" style="border-left:4px solid #6C4CF5;padding:14px 16px;margin:18px 0">
<b>PM takeaway:</b> path parameters answer one question: <i>which specific record are we working with?</i> When you write a requirement, name the ID that identifies the record, and state who may read it.
</div>

<h3 style="margin-top:22px">Path or query? A quick test</h3>
<p>Ask whether the value names a specific thing or only narrows a list. <code>/orders/123</code> names one order, so it is a path parameter. <code>/orders?status=shipped</code> narrows the list of orders, so it is a query parameter. Both can appear in one request: <code>GET /customers/456/orders?status=paid</code> means "paid orders for customer 456".</p>

<h2 class="sec-h" style="margin-top:34px">7. Query parameters: filtering and sorting</h2>
<p class="sub">Query parameters follow the <code>?</code>. They are <code>name=value</code> pairs joined by <code>&amp;</code>. They narrow or order the results, and do not change the method.</p>
{_pre('GET /orders?status=shipped&amp;sort=-created_at&amp;limit=20&amp;page=2')}
<ul>
<li><code>status=shipped</code>: only shipped orders</li>
<li><code>sort=-created_at</code>: newest first (the minus sign means descending)</li>
<li><code>limit=20</code>: 20 results per page</li>
<li><code>page=2</code>: the second page</li>
</ul>
<p>Spaces are encoded, so "New Delhi" becomes <code>New%20Delhi</code> in the address.</p>

<h2 class="sec-h" style="margin-top:34px">8. JSON: the format of the instructions</h2>
<p class="sub">JSON (JavaScript Object Notation) is the text format most APIs use for data. Four rules cover most cases:</p>
<ul>
<li><b>Objects</b> go in <code>{{ }}</code> and hold name and value pairs.</li>
<li><b>Lists</b> go in <code>[ ]</code>.</li>
<li><b>Text</b> is in double quotes: <code>"name": "Rahul Kumar"</code>.</li>
<li><b>Numbers, true, false and null</b> take no quotes: <code>"quantity": 2</code>. A trailing comma or a single quote makes the whole message invalid.</li>
</ul>
{_pre('{<br>  "customerId": 123,<br>  "productId": 456,<br>  "quantity": 2,<br>  "amount": 1500<br>}')}
<p>If <code>quantity</code> were sent as <code>"two"</code>, the API would reply <code>400 Bad Request</code>. The reply is JSON too, so the app can read the order ID and show it to the user.</p>

<h2 class="sec-h" style="margin-top:34px">9. Key takeaways</h2>
<div class="card" style="padding:16px 20px"><ul style="margin:0">
<li>An API is a set of rules for asking another program for something.</li>
<li>GET reads, POST creates, PUT replaces, PATCH changes some fields, DELETE removes.</li>
<li>Status codes tell you who has to act: 2xx success, 4xx the request or access, 5xx the server.</li>
<li>Endpoints are nouns in a clear hierarchy. Path parameters name one record; query parameters filter and sort.</li>
<li>JSON bodies are instructions the server checks before it acts.</li>
<li>Always ask: what happens if the request is repeated, and does the server check prices and permissions itself?</li>
</ul></div>

<h2 class="sec-h" style="margin-top:34px">10. Practice exercise</h2>
<div class="card" style="padding:16px 20px">
<ol>
<li>Write the request for a customer changing only their phone number. Choose the method and endpoint, and write the body.</li>
<li>A user reports "I can see my order but cannot cancel it" and the app shows an error. List three status codes that could explain it, and what each one tells the engineer.</li>
<li>Your payment step times out and the user taps Pay again. What can go wrong? Name the safeguard you would specify.</li>
<li>Write the request to show a customer's paid orders from last month. Mark which part is a path parameter and which parts are query parameters.</li>
</ol>
<p class="note">Check your answers against sections 2, 3, 4, 6 and the payment steps in section 2.</p>
</div>

<h2 class="sec-h" style="margin-top:34px">11. Quick check</h2>
<div class="card" style="padding:16px 20px">
<p><b>1. Which method should you use to update a customer's phone number only?</b><br>PATCH, because it changes selected fields. PUT would replace the whole record.</p>
<p><b>2. A request returns 401. What is the most likely cause?</b><br>The user is not logged in, or the login has expired. It is not a problem with the data.</p>
<p><b>3. In <code>GET /shipments/12345</code>, which part is the path parameter?</b><br>12345. It identifies the one shipment. <code>/shipments</code> names the resource type.</p>
<p><b>4. Why must the server check access even when the ID is valid?</b><br>Because a user can guess or change IDs. A valid ID does not prove the user is allowed to see that record.</p>
<p><b>5. Why should the server, not the app, set the order price?</b><br>The app can be changed by the user, so the server must recalculate the price from the product and quantity.</p>
</div>

<p class="foot" style="margin-top:34px;font-size:13px;color:#7a7a8c">Examples are simplified for learning. Real APIs differ in names, limits and error formats. Always read the documentation of the API you use.</p>
</div></section>"""
