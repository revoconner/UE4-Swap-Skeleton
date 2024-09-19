import maya.cmds as cmds
import maya.mel as mel

class UnrealAssetSwapSkeleton:
    def __init__(self):
        self.window_name = "UnrealAssetSwapSkeleton"
        self.text_fields = {}

    def create_ui(self):
        if cmds.window(self.window_name, exists=True):
            cmds.deleteUI(self.window_name)
        cmds.window(self.window_name, title="Unreal SK Swap Skeleton", width=300, height=200)
        main_layout = cmds.columnLayout(adjustableColumn=True)

        field_names = ["source", "target", "object"]
        for row in range(3):
            row_layout = cmds.rowLayout(numberOfColumns=3, adjustableColumn=2, parent=main_layout)
            cmds.text(label=field_names[row], parent=row_layout, width=50)
            text_field = cmds.textField(editable=False, parent=row_layout)
            cmds.button(label=field_names[row], command=lambda x, tf=text_field: self.store_object(tf), parent=row_layout, width=50)
            self.text_fields[field_names[row]] = text_field

        row_layout = cmds.rowLayout(numberOfColumns=1, adjustableColumn=1, parent=main_layout)
        cmds.button(label="transfer", command=self.transfer_skinned_joints, parent=row_layout, width=100)

        cmds.showWindow(self.window_name)

    def store_object(self, text_field):
        selection = cmds.ls(selection=True, long=True)
        if selection:
            object_name = selection[0]
            cmds.textField(text_field, edit=True, text=object_name)
        else:
            cmds.warning("No object selected. Please select an object in the outliner.")

    def transfer_skinned_joints(self, *args):
        object_name = cmds.textField(self.text_fields["object"], query=True, text=True)
        source_name = cmds.textField(self.text_fields["source"], query=True, text=True)
        target_name = cmds.textField(self.text_fields["target"], query=True, text=True)

        if not all([object_name, source_name, target_name]):
            cmds.warning("Please ensure all fields (object, source, target) are filled.")
            return

        cmds.select(cl=True)
        skinClusterStr = 'findRelatedSkinCluster("' + object_name + '")'
        skinCluster = mel.eval(skinClusterStr)
        #print(skinCluster)
        if skinCluster is not None:
            joints = cmds.skinCluster(skinCluster, query=True, inf=True)
            cmds.select(joints, add=True)
            sknJoints = cmds.ls(sl=True, long=True)
            #print("Selected joints:", sknJoints)
            
            for jointx in sknJoints:
                connections = cmds.listConnections(jointx, s=0, d=1, p=1, c=1)
                if connections:
                    filtered_connections = []
                    for i in range(0, len(connections), 2):
                        source = connections[i]
                        destination = connections[i+1]
                        if not any(word in source for word in ["scale", "message", "objectColorRGB"]):
                            filtered_connections.extend([source, destination])
                    
                    #print("Processing connections for {0}:".format(joint))
                    for i in range(0, len(filtered_connections), 2):
                        source_attr = filtered_connections[i]
                        dest_attr = filtered_connections[i+1]
                        
                        # Disconnect the attribute
                        cmds.disconnectAttr(source_attr, dest_attr)
                        #print("Disconnected: {0} -> {1}".format(source_attr, dest_attr))
                        
                        # Rename the attribute
                        new_source_attr = source_attr.replace(source_name, target_name)
                        #print("Renamed: {0} -> {1}".format(source_attr, new_source_attr))
                        
                        # Reconnect with the new name
                        try:
                            cmds.connectAttr(new_source_attr, dest_attr)
                            #print("Reconnected: {0} -> {1}".format(new_source_attr, dest_attr))
                        except Exception as e:
                            print("Error reconnecting: {0}".format(str(e)))
                else:
                    print("No connections found for {0}".format(jointx))
        else:
            print("-----> no skin on " + object_name + "!")

def run():
    ui = UnrealAssetSwapSkeleton()
    ui.create_ui()

if __name__ == "__main__":
    run()
