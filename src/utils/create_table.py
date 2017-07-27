#-*-coding:utf-8 -*-
import sys
import os

sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('../..'))

from src.utils.config_orm import metadata, engine

metadata.create_all(engine)
