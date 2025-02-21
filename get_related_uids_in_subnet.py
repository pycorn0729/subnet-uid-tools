"""
Get related uids in a subnet.
author: pycorn0729
"""

import bittensor as bt
from collections import defaultdict
from typing import List, Tuple, Dict

def _get_related_uids_in_subnet(
    ips_dict: dict,
    coldkeys_dict: dict,
    axon_infos: dict,
    subnet_uid: int,
    uid: int,
) -> List[Tuple[int, int]]:        
    bt.logging.info(f"Starting BFS from subnet_uid: {subnet_uid}, uid: {uid}")
    
    visited_dict: dict = {}
    queue = [(subnet_uid, uid)]
    related_uids = []
    visited_dict[(subnet_uid, uid)] = True
    
    while queue:
        current_subnet_uid, current_uid = queue.pop(0)
        bt.logging.info(f"Visiting subnet_uid: {current_subnet_uid}, uid: {current_uid}")
        
        current_axon_info = axon_infos.get((current_subnet_uid, current_uid), None)
        if current_axon_info is None:
            continue
            
        related_uids.append((current_subnet_uid, current_uid))
        
        coldkey = current_axon_info["coldkey"]
        ip = current_axon_info["ip"]
        
        # Add coldkey-related nodes to queue
        for next_subnet_uid, next_uid in coldkeys_dict.get(coldkey, []):
            if (next_subnet_uid, next_uid) not in visited_dict:
                queue.append((next_subnet_uid, next_uid))
                visited_dict[(next_subnet_uid, next_uid)] = True
                
        # Add IP-related nodes to queue
        for next_subnet_uid, next_uid in ips_dict.get(ip, []):
            if (next_subnet_uid, next_uid) not in visited_dict:
                queue.append((next_subnet_uid, next_uid))
                visited_dict[(next_subnet_uid, next_uid)] = True
                
    return related_uids


def get_related_uids_in_subnet(
    subtensor: bt.subtensor,
    subnet_uid: int,
    uid: int,
) -> Dict[str, int | List[int]]:    
    bt.logging.info(f"Getting related uids in subnet {subnet_uid} for uid {uid}")
    number_of_subnets = subtensor.metagraph(0).n.item()
    ips_dict = defaultdict(list)
    coldkeys_dict = defaultdict(list)
    axon_infos = {}
    
    bt.logging.info(
        f"\n"
        f"The number of subnets: {number_of_subnets}\n"
        f"Getting metagraph for all subnets..."
    )
    for _subnet_uid in range(1, number_of_subnets + 1):
        metagraph = subtensor.metagraph(_subnet_uid)
        number_of_uids = metagraph.n.item()
        for _uid in range(number_of_uids):
            ip = metagraph.addresses[_uid].split(":")[0]
            if ip != "/ipv0/0.0.0.0":
                ips_dict[ip].append((_subnet_uid, _uid))
            
            coldkey = metagraph.axons[_uid].coldkey
            coldkeys_dict[coldkey].append((_subnet_uid, _uid))

            axon_infos[(_subnet_uid, _uid)] = {
                "ip": ip,
                "coldkey": coldkey,
            }
    
    bt.logging.info(f"Getting related uids recursively")
    related_uids_in_all_subnets = _get_related_uids_in_subnet(
        ips_dict,
        coldkeys_dict,
        axon_infos,
        subnet_uid,
        uid,
    )
    related_uids_in_all_subnets = sorted(list(related_uids_in_all_subnets))
    related_uids = [
        _uid for _subnet_uid, _uid in related_uids_in_all_subnets if _subnet_uid == subnet_uid
    ]
    
    return {
        "total_uids_in_this_subnet": len(related_uids),
        "related_uids_in_this_subnet": related_uids,
        "total_uids_in_all_subnets": len(related_uids_in_all_subnets),
        "all_subnets_related_uids": related_uids_in_all_subnets,
    }

