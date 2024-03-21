import spotipy
import asyncio
import aioconsole
from spotipy.oauth2 import SpotifyOAuth

scope = "user-read-playback-state user-modify-playback-state"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


async def play():
    """Play music on Spotify."""
    sp.start_playback()
    print("Playback started")


async def pause():
    """Pause Spotify playback."""
    sp.pause_playback()
    print("Playback paused")


async def skip():
    """Play next track"""
    sp.next_track()
    print('Track skipped')


async def add_to_queue(uri):
    """Add track to queue"""
    sp.add_to_queue(uri)


async def search(q):
    """Search for track and return uri"""
    return sp.search(q)


async def search_add_to_queue(q):
    """Search for track, then add to queue"""
    response = await search(q)
    uri = response['tracks']['items'][0]['uri']
    await add_to_queue(uri)
    track = response['tracks']['items'][0]['name']
    artist = response['tracks']['items'][0]['artists'][0]['name']
    print(f'Added to Queue: {track} - {artist}')
    print()


async def handle_command(command):
    """Handle commands to control Spotify playback."""
    if command == 'play':
        await play()
    elif command == 'pause':
        await pause()
    elif command == 'skip':
        await skip()
    elif command[:3] == 'add':
        await search_add_to_queue(command[3:])
    else:
        print(f"Unknown command: {command}")


async def main():
    while True:
        command = await aioconsole.ainput("Enter command (play/pause): ")
        await handle_command(command.strip())


# Run the main function in the asyncio event loop
if __name__ == "__main__":
    asyncio.run(main())
