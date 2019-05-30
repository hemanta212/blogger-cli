'''Simplify logging creation no needed parameter '''
import logging
import os


class Logger:
    '''
    Customized logger class having get_logger method returning a logger

    params: [all are optional]
        name = Filename to pass generally it is __name__
        level = Specify level for filehandler (Warning is default)
        file = File to write log messages to (project.log is default)
        mode = Which mode to write. Default['a']
        debug_file = Specify debug file
        debug_mode = Specify which mode to use default['w']
        console [bool] = Switch console logging on or off.
    '''

    def __init__(self, name=None, level='warning', mode='a', debug_mode='w',
                 file=None, debug_file=None, console=False, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.level = self.__level_parser(level)
        self.file = file
        self.mode = mode
        self.debug_mode = debug_mode
        self.console = console
        self.debug_file = debug_file

    @staticmethod
    def __level_parser(key):
        '''
        logging attrs mapping to strs for easy parameter setting.
        param = 'debug', 'warning' etc in str
        output = logging.DEBUG, logging.Warning etc attributes
        '''
        level_dict = {
            'debug': logging.DEBUG,
            'warning': logging.WARNING,
            'error': logging.ERROR,
            'info': logging.INFO,
            'fatal': logging.FATAL,
            'critical': logging.CRITICAL,
        }
        return level_dict[key]

    @staticmethod
    def __handle_file(file):
        '''
        Checks if file exists else creates directory upto that file.
        Params:
            file : Input file
        '''
        if not os.path.exists(file):
            try:
                if os.path.split(file)[0] != '':
                    os.makedirs(os.path.split(file)[0])
            except FileExistsError:
                pass

    def get_logger(self):
        '''
        Returns a logger as specified in Logger class
        '''
        if self.name is None:
            import inspect
            caller = inspect.currentframe().f_back
            self.name = caller.f_globals['__name__']

        logger = logging.getLogger(self.name)
        logger.setLevel(logging.DEBUG)

        # create formatter
        format_style = '%(asctime)s : %(name)s: %(levelname)s : %(message)s'
        formatter = logging.Formatter(format_style)

        if self.console:
            # create console handler and set level to debug
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            # add formatter to console_handler
            console_handler.setFormatter(formatter)
            # add console_handler to logger
            logger.addHandler(console_handler)

        # create file handler and set level
        if self.file:
            self.__handle_file(self.file)
            filehandler = logging.FileHandler(self.file, mode=self.mode)
            filehandler.setLevel(self.level)
            filehandler.setFormatter(formatter)
            logger.addHandler(filehandler)

        if self.debug_file:
            self.__handle_file(self.debug_file)
            debug_filehandler = logging.FileHandler(
                self.debug_file, mode=self.debug_mode)
            debug_filehandler.setLevel(logging.DEBUG)
            debug_filehandler.setFormatter(formatter)
            logger.addHandler(debug_filehandler)
        return logger
