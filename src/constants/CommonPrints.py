import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def printEvent(event, handler: str):
    logger.debug('[{}] event: {}'.format(handler, event))
def printContext(context, handler: str):
    logger.debug('[{}] context: {}'.format(handler, context))