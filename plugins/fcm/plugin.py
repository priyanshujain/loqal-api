from django.conf import settings
from pyfcm import FCMNotification


class FcmPlugin(object):
    """
    Client implementation for the FCM.
    """

    def __init__(self, token):
        """
        Initializes an instance of the FCM client
        """

        self.fcm_token = token

    def send_notification(
        self,
        title=None,
        body=None,
        icon="https://res.cloudinary.com/dhqh3pewg/image/upload/v1614172092/favicon_1_hujfvh.png",
        data_message=None,
        sound=None,
        badge=None,
        low_priority=False,
        condition=None,
        time_to_live=None,
        click_action=None,
        collapse_key=None,
        delay_while_idle=False,
        restricted_package_name=None,
        dry_run=False,
        color=None,
        tag=None,
        body_loc_key=None,
        body_loc_args=None,
        title_loc_key=None,
        title_loc_args=None,
        content_available=None,
        extra_kwargs={},
        api_key=None,
        json_encoder=None,
        extra_notification_kwargs=None,
    ):

        """
        Copied from https://github.com/olucurious/PyFCM/blob/master/pyfcm/fcm.py:

        Send push notification to a single device
        Args:
            registration_id (str): FCM device registration IDs.
            body (str): Message string to display in the notification tray
            data (dict): Data message payload to send alone or with the notification
                message
            sound (str): The sound file name to play. Specify "Default" for device
                default sound.
        Keyword Args:
            collapse_key (str, optional): Identifier for a group of messages
                that can be collapsed so that only the last message gets sent
                when delivery can be resumed. Defaults to ``None``.
            delay_while_idle (bool, optional): If ``True`` indicates that the
                message should not be sent until the device becomes active.
            time_to_live (int, optional): How long (in seconds) the message
                should be kept in FCM storage if the device is offline. The
                maximum time to live supported is 4 weeks. Defaults to ``None``
                which uses the FCM default of 4 weeks.
            low_priority (boolean, optional): Whether to send notification with
                the low priority flag. Defaults to ``False``.
            restricted_package_name (str, optional): Package name of the
                application where the registration IDs must match in order to
                receive the message. Defaults to ``None``.
            dry_run (bool, optional): If ``True`` no message will be sent but
                request will be tested.

        Returns:
            :tuple:`multicast_id(long), success(int), failure(int),
                canonical_ids(int), results(list)`:
            Response from FCM server.
        Raises:
            AuthenticationError: If :attr:`api_key` is not set or provided or there
                is an error authenticating the sender.
            FCMServerError: Internal server error or timeout error on Firebase cloud
                messaging server
            InvalidDataError: Invalid data provided
            InternalPackageError: JSON parsing error, mostly from changes in the
                response of FCM, create a new github issue to resolve it.
        """
        if api_key is None:
            api_key = settings.FCM_SERVER_KEY
        push_service = FCMNotification(
            api_key=api_key, json_encoder=json_encoder
        )
        result = push_service.notify_single_device(
            registration_id=self.fcm_token,
            message_title=title,
            message_body=body,
            message_icon=icon,
            data_message=data_message,
            sound=sound,
            badge=badge,
            collapse_key=collapse_key,
            low_priority=low_priority,
            condition=condition,
            time_to_live=time_to_live,
            click_action=click_action,
            delay_while_idle=delay_while_idle,
            restricted_package_name=restricted_package_name,
            dry_run=dry_run,
            color=color,
            tag=tag,
            body_loc_key=body_loc_key,
            body_loc_args=body_loc_args,
            title_loc_key=title_loc_key,
            title_loc_args=title_loc_args,
            content_available=content_available,
            extra_kwargs=extra_kwargs,
            extra_notification_kwargs=extra_notification_kwargs,
        )

        # do not raise errors, pyfcm will raise exceptions if response status will
        # be anything but 200

        return result

    def send_data(
        self,
        condition=None,
        collapse_key=None,
        delay_while_idle=False,
        time_to_live=None,
        restricted_package_name=None,
        low_priority=False,
        dry_run=False,
        data_message=None,
        content_available=None,
        api_key=None,
        timeout=5,
        json_encoder=None,
        extra_notification_kwargs=None,
    ):
        """
        Send push message to a single device
        All arguments correspond to that defined in pyfcm/fcm.py.

        Args:
            registration_id (str): FCM device registration IDs.
            data_message (dict): Data message payload to send alone or with the
                notification message

        Keyword Args:
            collapse_key (str, optional): Identifier for a group of messages
                that can be collapsed so that only the last message gets sent
                when delivery can be resumed. Defaults to ``None``.
            delay_while_idle (bool, optional): If ``True`` indicates that the
                message should not be sent until the device becomes active.
            time_to_live (int, optional): How long (in seconds) the message
                should be kept in FCM storage if the device is offline. The
                maximum time to live supported is 4 weeks. Defaults to ``None``
                which uses the FCM default of 4 weeks.
            low_priority (boolean, optional): Whether to send notification with
                the low priority flag. Defaults to ``False``.
            restricted_package_name (str, optional): Package name of the
                application where the registration IDs must match in order to
                receive the message. Defaults to ``None``.
            dry_run (bool, optional): If ``True`` no message will be sent but
                request will be tested.
            timeout (int, optional): set time limit for the request
        Returns:
            :dict:`multicast_id(long), success(int), failure(int),
                canonical_ids(int), results(list)`:
            Response from FCM server.

        Raises:
            AuthenticationError: If :attr:`api_key` is not set or provided or there
                is an error authenticating the sender.
            FCMServerError: Internal server error or timeout error on Firebase cloud
                messaging server
            InvalidDataError: Invalid data provided
            InternalPackageError: Mostly from changes in the response of FCM,
                contact the project owner to resolve the issue
        """
        push_service = FCMNotification(
            api_key=settings.FCM_SERVER_KEY if api_key is None else api_key,
            json_encoder=json_encoder,
        )
        return push_service.single_device_data_message(
            registration_id=self.fcm_token,
            condition=condition,
            collapse_key=collapse_key,
            delay_while_idle=delay_while_idle,
            time_to_live=time_to_live,
            restricted_package_name=restricted_package_name,
            low_priority=low_priority,
            dry_run=dry_run,
            data_message=data_message,
            content_available=content_available,
            timeout=timeout,
            extra_notification_kwargs=extra_notification_kwargs,
        )
