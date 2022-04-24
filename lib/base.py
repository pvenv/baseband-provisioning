import re

def replace_atributes_in_files(self, bts_name, bts_oam, bts_ip_bts, bts_ip_mbh, tn_port):
    
    with open('sftp\\Universal_SiteBasicFileOAM.xml', 'r') as f:
        rbs_summary_file_text = f.read()
        f.close()
    with open('sftp\\Universal_SiteBasicFileOAM.xml', 'w') as f:
        rbs_summary_file_text = re.sub(r'\<fingerprint\>\w+\<\/fingerprint\>', f'<fingerprint>BTS_56_{bts_name}</fingerprint>', rbs_summary_file_text)
        rbs_summary_file_text = re.sub(r'\<tnPortId\>\w+\<\/tnPortId\>', f'<tnPortId>TN_{tn_port}</tnPortId>', rbs_summary_file_text)
        rbs_summary_file_text = re.sub(r'TnPort\=\w+\<\/encapsulation\>', f'TnPort=TN_{tn_port}</encapsulation>', rbs_summary_file_text)
        rbs_summary_file_text = re.sub(r'\<address\>\d+\.\d+\.\d+\.\d+\/30\<\/address\>', f'<address>{bts_ip_bts}/30</address>', rbs_summary_file_text)
        rbs_summary_file_text = re.sub(r'\<networkManagedElementId\>\w+\<\/networkManagedElementId\>', f'<networkManagedElementId>BTS_56_{bts_name}</networkManagedElementId>', rbs_summary_file_text)
        rbs_summary_file_text = re.sub(r'<vlanId>\d+</vlanId>', f'<vlanId>{bts_oam}</vlanId>', rbs_summary_file_text)
        f.write(rbs_summary_file_text)
        f.close()
        self.form.plainTextEdit.appendHtml(f'Файл Universal_SiteBasicFileOAM.xml успешно обновлен!')
    
    with open('sftp\\Universal_SiteEquipmentFileMPclusterCabinet.xml', 'r') as f:
        equipment_file_text = f.read()
        f.close()
    with open('sftp\\Universal_SiteEquipmentFileMPclusterCabinet.xml', 'w') as f:
        equipment_file_text = re.sub(r'\<tnPortId\>\w+\<\/tnPortId\>', f'<tnPortId>TN_{tn_port}</tnPortId>', equipment_file_text)
        f.write(equipment_file_text)
        f.close()
        self.form.plainTextEdit.appendHtml(f'Файл Universal_SiteEquipmentFileMPclusterCabinet.xml успешно обновлен!')
    
    return True