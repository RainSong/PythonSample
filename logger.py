# -*- config:utf-8 -*-

import logging



# logger = logging.getLogger( 'spiter' )
logger = logging.getLogger()
logger.setLevel( logging.WARNING )

# log format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s') 
  
# file log
# fh = logging.FileHandler('log.log')  
# fh.setLevel( logging.DEBUG )  
# fh.setFormatter(formatter) 
# logger.addHandler(fh)
  
# console log 
ch = logging.StreamHandler()  
ch.setLevel( logging.WARNING )
ch.setFormatter( formatter )  
logger.addHandler(ch)
