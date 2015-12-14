import logging
from sfmutils.consumer import BaseConsumer
from ui.models import Harvest, SeedSet

log = logging.getLogger(__name__)


class SfmUiConsumer(BaseConsumer):
    """
    Class for the SFM UI Consumer, which subscribes to
    messages from the queue and updates the models as appropriate.
    """
    def on_message(self):
        # TODO: Currently assumes message is a harvest status message.
        #       We'll want to check the routing key before processing,
        #       as on_message will likely be invoked for various
        #       key bindings in the future.
        m = self.message
        m_id = m['id']
        m_status = m['status']
        m_date_started = m['date_started']
        m_date_ended = m['date_ended']

        ss = SeedSet(id=m_id)
        h = Harvest(seed_set=ss, stats=m_status,
                    date_started=m_date_started, date_ended=m_date_ended)
        h.save()
