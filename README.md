# UE4 Swap Skeleto
Merge skeleton of modular assets when importing into Maya to bypass multiple groups that are created with their own skeleton

### When importing multiple objects inside Maya after exporting from unreal engine, they come in their own groups. So even if the skeleton was shared among these skeletal meshes, inside of Maya they will have their own skeleton grouped together with the object.
### This tool helps you to change the asset skeleton of the mesh while retaining weights to one skeleton in the scene.

## How to work?
1. Select the target group from outliner and press the button (This is the group that has the skeleton you want your mesh to be rigged to)
2. Select the source group from the outliner and press the button (this is the group that the object is a part of at the moment)
3. Select the object
4. Hit transfer.
5. The object is now skinned to the skeleton inside target group. You can move your object to be a part of the group and delete the other group entirely with the skeleton.

![image](https://github.com/user-attachments/assets/8e57e402-17dc-47d3-a6bc-129ac137e2c7)
