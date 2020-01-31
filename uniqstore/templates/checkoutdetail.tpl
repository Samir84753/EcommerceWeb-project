{% extends "mail_templated/base.tpl" %}

{% block subject %}
Uniqlo Store checkout message
{% endblock %}

{% block body %}
This is a plain text part.
{% endblock %}

{% block html %}

<p>Hey {{user}},</p>
<p>We have received your order request successfully.</p>
<p>You will be getting a call from our delivery team for confirmation soon.</p>
<p>Greetings,</p>
<p>Team Uniqlo Store</p>
{% endblock %}