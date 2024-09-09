import logging

def logger_init(name):
    logger = logging.getLogger(name)
    # configuring our specific logger
    # setting the log level for the logger
    logger.setLevel(logging.DEBUG)
    # creating a formatter
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
    file_handler = logging.FileHandler('all.log')
    # adding the formatting to the file handler
    file_handler.setFormatter(formatter)
    # to display the result in the console
    stream_handler = logging.StreamHandler()
    # adding the formatting to the stream handler
    stream_handler.setFormatter(formatter)
    # adding file handler and stream_handler to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger