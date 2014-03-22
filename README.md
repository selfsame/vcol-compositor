vcol-compositor
===============

A Blender addon for baking and compositing vertex color layers.

Fancy page at http://selfsamegames.com/vertex/

## installation

You can install the addon by placing it in the Blender/2.68/scripts/addons directory or by clicking "install from file" in user preferences. Once installed, make sure it's activated. The addon is called ```Render: Vertex Diffuse Bake```

## usage

the Vertex Bake UI is in the Render buttons panel

the combined vertex results are written to the 'Col' layer, you should have this layer set to visible, but not part of the bake stack

light and ao baking writes to LIGHT and AO layers (they should be created automatically), but you can set a custom target in the Vertex Bake UI panel (as long as it's an existing layer!)

```add layer pass``` will add a layer to the mixing stack, you can change the source vcol data.

Use the edge split modifier to get hard edges for vetex light baking

You have to rebake lighting and/or ao every time you make changes to the scene

if you want to save the combined output, rename the Col layer and make a new 'Col' to replace it.

When using GLSL shading mode, you'll need to check 'Vertex Color Paint' in the object material buttons to see vertex colors in the viewport

typically you want to set the material to 'shadeless' so see the vcol output without realtime lighting applied

A basic stack recipie is to mix ao and lighting, then multiply a color layer

remember you can still paint manually on any of the layers, this is useful for removing AO artifacts and other fine tweaks
