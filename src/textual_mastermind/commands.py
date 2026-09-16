from functools import partial
from importlib.metadata import metadata
from typing import cast

from textual.command import DiscoveryHit, Hit, Hits, Provider

from .app_config import app_config

pkg_name = cast(str, __package__)
pkg_metadata = metadata(pkg_name)


class AboutCommand(Provider):
    help_str = "About Mastermind"
    email_str = pkg_metadata["Author-email"].split("<")[1][:-1]
    notify_str = (
        f"[bold][cornflowerblue]{app_config.ui['title']}[/][/] {pkg_metadata['Version']}\n"
        f"{pkg_metadata['Author']}\n"
        f"[link='mailto:{email_str}']{email_str}[/]"
    )

    async def search(self, query: str) -> Hits:
        matcher = self.matcher(query)
        command = "About"
        score = matcher.match(command)
        if score > 0:
            yield Hit(
                score,
                matcher.highlight(command),
                partial(self.app.notify, self.notify_str),
                help=self.help_str,
            )

    async def discover(self) -> Hits:
        yield DiscoveryHit(
            "About",
            partial(self.app.notify, self.notify_str),
            help=self.help_str,
        )
