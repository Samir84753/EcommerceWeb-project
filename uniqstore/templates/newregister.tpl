{% extends "mail_templated/base.tpl" %}

{% block subject %}
New account Registration for {{user}}
{% endblock %}

{% block body %}
This is a plain text part.
{% endblock %}

{% block html %}

<p>Hey {{user}},</p>
<p><br>Your account has been successfully registered,Happy Shopping.</p>
<p>Greetings,</p>
<p>Team Uniqlo Store</p>
{% endblock %}