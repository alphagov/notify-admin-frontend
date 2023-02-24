from flask import (
    abort,
    current_app,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user
from notifications_utils.recipients import RecipientCSV
from notifications_utils.template import HTMLEmailTemplate, LetterImageTemplate

from app import letter_branding_client, status_api_client
from app.formatters import message_count
from app.main import main
from app.main.forms import FieldWithNoneOption
from app.main.views.pricing import CURRENT_SMS_RATE
from app.main.views.sub_navigation_dictionaries import features_nav, using_notify_nav
from app.models.branding import EmailBranding


@main.route("/")
def index():

    if current_user and current_user.is_authenticated:
        return redirect(url_for("main.choose_account"))

    return render_template(
        "views/signedout.html",
        sms_rate=CURRENT_SMS_RATE,
        counts=status_api_client.get_count_of_live_services_and_organisations(),
    )


@main.route("/error/<int:status_code>")
def error(status_code):
    if status_code >= 500:
        abort(404)
    abort(status_code)


@main.route("/cookies")
def cookies():
    return render_template("views/cookies.html")


@main.route("/privacy")
def privacy():
    return render_template("views/privacy.html")


@main.route("/accessibility-statement")
def accessibility_statement():
    return render_template("views/accessibility_statement.html")


@main.route("/delivery-and-failure")
@main.route("/features/messages-status")
def delivery_and_failure():
    return redirect(url_for(".guidance_message_status"), 301)


@main.route("/design-patterns-content-guidance")
def design_content():
    return redirect("https://www.gov.uk/service-manual/design/sending-emails-and-text-messages", 301)


@main.route("/_email")
def email_template():
    branding_style = request.args.get("branding_style")

    if not branding_style or branding_style in {"govuk", FieldWithNoneOption.NONE_OPTION_VALUE}:
        branding = EmailBranding.govuk_branding()

    elif branding_style == "custom":
        branding = EmailBranding.with_default_values(**request.args)

    else:
        branding = EmailBranding.from_id(branding_style)

    template = {
        "template_type": "email",
        "subject": "Email branding preview",
        "content": render_template("example-email.md"),
    }

    resp = make_response(
        str(
            HTMLEmailTemplate(
                template,
                govuk_banner=branding.has_govuk_banner,
                brand_text=branding.text,
                brand_colour=branding.colour,
                brand_logo=branding.logo_url,
                brand_banner=branding.has_brand_banner,
                brand_alt_text=branding.alt_text,
            )
        )
    )

    resp.headers["X-Frame-Options"] = "SAMEORIGIN"
    return resp


@main.route("/_letter")
def letter_template():
    branding_style = request.args.get("branding_style")
    filename = request.args.get("filename")

    if branding_style == FieldWithNoneOption.NONE_OPTION_VALUE:
        branding_style = None
    if filename == FieldWithNoneOption.NONE_OPTION_VALUE:
        filename = None

    if branding_style:
        if filename:
            abort(400, "Cannot provide both branding_style and filename")
        filename = letter_branding_client.get_letter_branding(branding_style)["filename"]
    elif not filename:
        filename = "no-branding"

    template = {"subject": "", "content": "", "template_type": "letter"}
    image_url = url_for("no_cookie.letter_branding_preview_image", filename=filename)

    template_image = str(
        LetterImageTemplate(
            template,
            image_url=image_url,
            page_count=1,
        )
    )

    resp = make_response(render_template("views/service-settings/letter-preview.html", template=template_image))

    resp.headers["X-Frame-Options"] = "SAMEORIGIN"
    return resp


@main.route("/integration-testing")
def integration_testing():
    return redirect(url_for("main.guidance_api_documentation"), 301)


@main.route("/callbacks")
def callbacks():
    return redirect(url_for("main.guidance_api_documentation"), 301)


@main.route("/terms-of-use", endpoint="terms_of_use")
def terms_of_use():
    return render_template("views/terms-of-use.html")


# --- Guidance pages --- #


@main.route("/features")
def guidance_features():
    return render_template("views/guidance/features/index.html", navigation_links=features_nav())


@main.route("/features/roadmap")
def guidance_roadmap():
    return render_template("views/guidance/features/roadmap.html", navigation_links=features_nav())


@main.route("/features/security")
def guidance_security():
    return render_template("views/guidance/features/security.html", navigation_links=features_nav())


@main.route("/features/who-its-for")
def guidance_who_its_for():
    return redirect(url_for(".guidance_who_can_use_notify"), 301)


@main.route("/features/who-can-use-notify")
def guidance_who_can_use_notify():
    return render_template(
        "views/guidance/features/who-can-use-notify.html",
        navigation_links=features_nav(),
    )


@main.route("/using-notify")
def guidance_using_notify():
    return render_template(
        "views/guidance/using-notify/index.html",
        navigation_links=using_notify_nav(),
    )


@main.route("/using-notify/api-documentation")
def guidance_api_documentation():
    return render_template(
        "views/guidance/using-notify/api-documentation.html",
        navigation_links=using_notify_nav(),
    )


@main.route("/using-notify/bulk-sending")
def guidance_bulk_sending():
    return render_template(
        "views/guidance/using-notify/bulk-sending.html",
        max_spreadsheet_rows=RecipientCSV.max_rows,
        rate_limits=[
            message_count(limit, channel)
            for channel, limit in current_app.config["DEFAULT_LIVE_SERVICE_RATE_LIMITS"].items()
        ],
        navigation_links=using_notify_nav(),
    )


@main.route("/using-notify/message-status")
@main.route("/using-notify/message-status/<template_type:notification_type>")
def guidance_message_status(notification_type=None):
    if not notification_type:
        return redirect(url_for(".guidance_message_status", notification_type="email"))
    return render_template(
        "views/guidance/using-notify/message-status.html",
        navigation_links=using_notify_nav(),
        notification_type=notification_type,
    )


@main.route("/using-notify/delivery-times")
def guidance_delivery_times():
    return render_template(
        "views/guidance/using-notify/delivery-times.html",
        navigation_links=using_notify_nav(),
    )


@main.route("/using-notify/email-branding")
def guidance_email_branding():
    return render_template(
        "views/guidance/using-notify/email-branding.html",
        navigation_links=using_notify_nav(),
    )


@main.route("/using-notify/formatting")
def guidance_formatting():
    return render_template(
        "views/guidance/using-notify/formatting.html",
        navigation_links=using_notify_nav(),
    )


@main.route("/using-notify/letter-branding")
def guidance_letter_branding():
    return render_template(
        "views/guidance/using-notify/letter-branding.html",
        navigation_links=using_notify_nav(),
    )


@main.route("/using-notify/optional-content")
def guidance_optional_content():
    return render_template(
        "views/guidance/using-notify/optional-content.html",
        navigation_links=using_notify_nav(),
    )


@main.route("/using-notify/personalisation")
def guidance_personalisation():
    return render_template(
        "views/guidance/using-notify/personalisation.html",
        navigation_links=using_notify_nav(),
    )


@main.route("/using-notify/receive-text-messages")
def guidance_receive_text_messages():
    return render_template(
        "views/guidance/using-notify/receive-text-messages.html",
        navigation_links=using_notify_nav(),
    )


@main.route("/using-notify/reply-to-email-address")
def guidance_reply_to_email_address():
    return render_template(
        "views/guidance/using-notify/reply-to-email-address.html",
        navigation_links=using_notify_nav(),
    )


@main.route("/using-notify/schedule-messages")
def guidance_schedule_messages():
    return render_template(
        "views/guidance/using-notify/schedule-messages.html",
        navigation_links=using_notify_nav(),
    )


@main.route("/using-notify/send-files-by-email")
def guidance_send_files_by_email():
    return render_template(
        "views/guidance/using-notify/send-files-by-email.html",
        navigation_links=using_notify_nav(),
    )


@main.route("/using-notify/team-members-and-permissions")
def guidance_team_members_and_permissions():
    return render_template(
        "views/guidance/using-notify/team-members-permissions.html",
        navigation_links=using_notify_nav(),
    )


@main.route("/using-notify/templates")
def guidance_templates():
    return render_template(
        "views/guidance/using-notify/templates.html",
        navigation_links=using_notify_nav(),
    )


@main.route("/using-notify/text-message-sender")
def guidance_text_message_sender():
    return render_template(
        "views/guidance/using-notify/text-message-sender.html",
        navigation_links=using_notify_nav(),
    )


@main.route("/using-notify/upload-a-letter")
def guidance_upload_a_letter():
    return render_template(
        "views/guidance/using-notify/upload-a-letter.html",
        navigation_links=using_notify_nav(),
    )


# --- Redirects --- #


@main.route("/roadmap", endpoint="old_roadmap")
@main.route("/terms", endpoint="old_terms")
@main.route("/information-security", endpoint="information_security")
@main.route("/guidance_using_notify", endpoint="old_using_notify")
@main.route("/using-notify/guidance/schedule-emails-and-text-messages", endpoint="old_schedule_messages")
@main.route("/using-notify/guidance/branding-and-customisation", endpoint="old_branding_and_customisation")
@main.route("/information-risk-management", endpoint="information_risk_management")
@main.route("/integration_testing", endpoint="old_integration_testing")
@main.route("/features/sms", endpoint="old_features_sms")
@main.route("/features/email", endpoint="old_features_email")
@main.route("/features/letters", endpoint="old_features_letters")
@main.route("/features/terms", endpoint="old_features_terms")
@main.route("/using-notify/who-can-use-notify", endpoint="old_who_can_use_notify")
@main.route("/using-notify/who-its-for", endpoint="old_who_its_for")
@main.route("/using-notify/delivery-status", endpoint="old_delivery_status")
@main.route("/using-notify/guidance/letter-specification", endpoint="old_letter_specification")
@main.route("/features/using-notify", endpoint="old_features_using_notify")
@main.route("/trial-mode", endpoint="old_trial_mode")
@main.route("/features/trial-mode", endpoint="old_trial_mode")
@main.route("/using-notify/trial-mode", endpoint="old_trial_mode")
@main.route("/using-notify/guidance", endpoint="old_guidance_index")
@main.route("/documentation", endpoint="old_api_documentation")
@main.route("/using-notify/guidance/bulk-sending", endpoint="old_bulk_sending")
@main.route("/using-notify/guidance/delivery-times", endpoint="old_delivery_times")
@main.route("/using-notify/guidance/email-branding", endpoint="old_email_branding")
@main.route("/using-notify/guidance/edit-and-format-messages", endpoint="old_edit_and_format_messages")
@main.route("/using-notify/guidance/letter-branding", endpoint="old_letter_branding")
@main.route("/using-notify/guidance/optional-content", endpoint="old_optional_content")
@main.route("/using-notify/guidance/personalisation", endpoint="old_personalisation")
@main.route("/using-notify/guidance/receive-text-messages", endpoint="old_receive_text_messages")
@main.route("/using-notify/guidance/reply-to-email-address", endpoint="old_reply_to_email_address")
@main.route("/using-notify/guidance/schedule-messages", endpoint="old_schedule_messages")
@main.route("/using-notify/guidance/send-files-by-email", endpoint="old_send_files_by_email")
@main.route("/using-notify/guidance/team-members-and-permissions", endpoint="old_team_members_and_permissions")
@main.route("/using-notify/guidance/templates", endpoint="old_templates")
@main.route("/using-notify/guidance/text-message-sender", endpoint="old_text_message_sender")
@main.route("/using-notify/guidance/upload-a-letter", endpoint="old_upload_a_letter")
@main.route("/performance", endpoint="old_performance")
@main.route("/using-notify/get-started", endpoint="old_using_notify_get_started")
@main.route("/features/get-started", endpoint="old_features_get_started")
def old_page_redirects():
    redirects = {
        "main.old_roadmap": "main.guidance_roadmap",
        "main.old_terms": "main.terms_of_use",
        "main.information_security": "main.guidance_security",
        "main.information_risk_management": "main.guidance_security",
        "main.old_integration_testing": "main.integration_testing",
        "main.old_schedule_messages": "main.guidance_schedule_messages",
        "main.old_branding_and_customisation": "main.guidance_using_notify",
        "main.old_features_sms": "main.guidance_features",
        "main.old_features_email": "main.guidance_features",
        "main.old_features_letters": "main.guidance_features",
        "main.old_features_terms": "main.terms_of_use",
        "main.old_who_can_use_notify": "main.guidance_who_can_use_notify",
        "main.old_who_its_for": "main.guidance_who_its_for",
        "main.old_delivery_status": "main.guidance_message_status",
        "main.old_letter_specification": "main.guidance_upload_a_letter",
        "main.old_features_using_notify": "main.guidance_using_notify",
        "main.old_using_notify": "main.guidance_using_notify",
        "main.old_trial_mode": "main.guidance_trial_mode",
        "main.old_guidance_index": "main.guidance_using_notify",
        "main.old_api_documentation": "main.guidance_api_documentation",
        "main.old_bulk_sending": "main.guidance_bulk_sending",
        "main.old_delivery_times": "main.guidance_delivery_times",
        "main.old_edit_and_format_messages": "main.guidance_formatting",
        "main.old_email_branding": "main.guidance_email_branding",
        "main.old_letter_branding": "main.guidance_letter_branding",
        "main.old_optional_content": "main.guidance_optional_content",
        "main.old_personalisation": "main.guidance_personalisation",
        "main.old_receive_text_messages": "main.guidance_receive_text_messages",
        "main.old_reply_to_email_address": "main.guidance_reply_to_email_address",
        "main.old_send_files_by_email": "main.guidance_send_files_by_email",
        "main.old_team_members_and_permissions": "main.guidance_team_members_and_permissions",
        "main.old_templates": "main.guidance_templates",
        "main.old_text_message_sender": "main.guidance_text_message_sender",
        "main.old_upload_a_letter": "main.guidance_upload_a_letter",
        "main.old_performance": "main.performance",
        "main.old_using_notify_get_started": "main.guidance_features",
        "main.old_features_get_started": "main.guidance_features",
    }
    return redirect(url_for(redirects[request.endpoint]), code=301)


# need to handle this separately to the other redirects due to dynamic notification type
@main.route("/using-notify/guidance/message-status")
@main.route("/using-notify/guidance/message-status/<template_type:notification_type>")
def old_message_status(notification_type=None):
    return redirect(url_for("main.guidance_message_status", notification_type=notification_type), code=301)


@main.route("/docs/notify-pdf-letter-spec-latest.pdf")
def letter_spec():
    return redirect("https://docs.notifications.service.gov.uk" "/documentation/images/notify-pdf-letter-spec-v2.4.pdf")
