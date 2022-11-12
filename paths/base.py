import logging

logger = logging.getLogger(__name__)


class AreaMovementBase(object):
    checkpoint_fallback = {}

    @classmethod
    def execute(cls, checkpoint):
        # If we have a message here, something has probably gone wrong
        if message := cls.checkpoint_fallback.get(checkpoint):
            logger.warning(f"[{cls.__name__} | fallback]: {message}")
        return cls.checkpoint_coordiantes.get(checkpoint, [999, 999])
