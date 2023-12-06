# Prizefighter Dev Suite

## Overview

This [Blender](https://www.blender.org/) addon is a tool developed for use with my Roblox games, particularly [Prizefighter](https://www.roblox.com/games/4735589050/Prizefighter-Closed-Beta). It provides a streamlined workflow to export animations in a custom text format that seamlessly integrates with Prizefighter's custom animation system. Utilized by all three developers, it drastically accelerates animation import times by up to 90%, while also improving the animation creation and editing processes. I developed this back in late 2021. It was my first real project in Python and I thought it would be nice to share :)

## Features

- **Bone locking:** Create IK-like constraints while using FK, with config saving and loading.
- **Offset system:** Easily adjust many animation poses at once.
- **Export animations:** Convert .fbx into a custom Roblox-supported format. Animation names can create automatic directories, e.g, `"Combat/DefaultStyle/Idle"` 
- **Model visibility toggles:** Easily toggle the visibility of models on the character to adjust the workflow.
- **FPS slider:** Used to slow down the playback of an animation for more precise editing.
  
## To do

- Make the bone config editable from the plugin itself.
- Ability to edit the models that the visibility toggles adjust.
- Broaden the scope of the addon and provide documentation.

## License

This addon is released under the GNU General Public License (GPL). See the LICENSE file for details.
