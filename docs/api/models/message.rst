.. currentmodule:: apraw.models

Message
=======

This section describes the usage and members of the Message model.

Messages are the private messages sent and received via the old Reddit private messaging system and are conventionally
retrieved through the inbox:

.. code-block:: python3

    async for message in reddit.user.inbox.unread():
        print(message)

.. autoclass:: Message
    :members:
    :inherited-members:
