import asyncio
import dataclasses
import json
import logging
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class Session:
    student_ident: str
    period: float
    last_ts: float
    last_question: str


class Manager:
    def __init__(self, filename: str, handler=None, delay=10):
        self.filename = filename
        self.sessions = {}
        self.load_from_file(filename)
        self._dirty = False
        self.handler = handler
        self.sleep_delay = delay

    def __del__(self):
        self.auto_save()

    def auto_save(self):
        if self._dirty:
            self.save_file(self.filename)
            self._dirty = False

    def load_from_file(self, filename: str):
        self.sessions = {}
        try:
            with open(filename, 'r') as f:
                json_data = json.load(f)
                for ident, data in json_data.items():
                    self.sessions[ident] = Session(**data)
            logger.info(f'Loaded {len(self.sessions)} sessions')
        except FileNotFoundError:
            logger.warning(f'File {filename} not found')
        except json.JSONDecodeError:
            logger.warning(f'File {filename} is not a valid JSON file')

    def save_file(self, filename: str):
        logger.info(f'Saving {len(self.sessions)} sessions to {filename!r}')
        with open(filename, 'w') as f:
            data = {
                ident: dataclasses.asdict(obj) for ident, obj in self.sessions.items()
            }
            json.dump(data, f, indent=4)

    def register_student(self, ident: str, period: float, save: bool = True):
        if period < 60:
            raise ValueError('Period must be at least 60 seconds')

        if ident in self.sessions:
            session = self.sessions[ident]
            session.period = period
        else:
            session = Session(ident, period, 0, '')
            self.sessions[ident] = session

        logger.info(f'Student {ident} registered with period {period:.1f} sec')

        self._dirty = True
        if save:
            self.auto_save()

    def unregister_student(self, ident: str):
        if ident in self.sessions:
            del self.sessions[ident]
            self._dirty = True
            self.auto_save()
            logging.info(f'Student {ident} unregistered')

    async def on_timer(self, session: Session):
        ident = session.student_ident
        logger.info(f'Timer for {ident} expired; firing event!')
        if handler := self.handler:
            new_session = await handler(session)
            if new_session is None:
                self.unregister_student(ident)
                return

            new_session.last_ts = datetime.now().timestamp()

            self.sessions[ident] = new_session
            self._dirty = True
            logger.info(f'Session data updated for {ident}: {new_session}')

    async def tick(self):
        logger.info(f'Tick: {len(self.sessions)} sessions')
        now = datetime.now().timestamp()
        for ident in list(self.sessions):
            session = self.sessions[ident]
            if now - session.last_ts > session.period:
                await self.on_timer(session)

        self.auto_save()

    async def main_loop(self):
        while True:
            await self.tick()
            await asyncio.sleep(max(1, self.sleep_delay))

    async def run_in_background(self, *args, **kwargs):
        asyncio.create_task(self.main_loop())

    def get_session(self, ident: str) -> Session:
        return self.sessions.get(ident)
