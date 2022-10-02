import bpy

ANIMATIONS_PATH = 'D:/artykuly/wat_2/test_animations'
object = 'deer'
output_path = ANIMATIONS_PATH + '/' + object + '/'

print(output_path)

scene = bpy.context.scene
scene.render.filepath = output_path