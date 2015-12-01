# -*- coding: utf-8 -*-
__author__ = 'Abbott'

from contextlib import contextmanager
from sqlalchemy.orm import Session
from . import tables, logger


@contextmanager
def GetSession():
    """
    @note 生成session
    @return: Session类实例
    """
    session = Session()
    try:
        yield session
    except Exception, err:
        session.rollback()
        logger.error('====== db_session - GetSession : err start')
        logger.error(err)
        logger.error('====== db_session - GetSession : err end')
    else:
        session.commit()
    finally:
        session.close()