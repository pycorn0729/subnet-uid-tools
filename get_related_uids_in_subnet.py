"""
Get related uids in a subnet.
author: pycorn0729
"""

import bittensor as bt
from typing import List, Tuple, Dict


def _get_related_uids_in_subnet(
    ips_dict: dict,
    coldkeys_dict: dict,
    axon_infos: dict,
    subnet_uid: int,
    uid: int,
    visited_dict: dict = {},
) -> List[Tuple[int, int]]:    
    axon_info = axon_infos.get((subnet_uid, uid), None)
    if axon_info is None:
        return []
    
    if (subnet_uid, uid) in visited_dict:
        return []
    
    bt.logging.info(f"Visiting subnet_uid: {subnet_uid}, uid: {uid}")
    
    visited_dict[(subnet_uid, uid)] = True
    related_uids = [(subnet_uid, uid)]
    coldkey = axon_info["coldkey"]
    ip = axon_info["ip"]
    
    for subnet_uid, uid in coldkeys_dict.get(coldkey, []):
        related_uids.extend(
            _get_related_uids_in_subnet(
                ips_dict,
                coldkeys_dict,
                axon_infos,
                subnet_uid,
                uid,
            )
        )

    for subnet_uid, uid in ips_dict.get(ip, []):
        related_uids.extend(
            _get_related_uids_in_subnet(
                ips_dict,
                coldkeys_dict,
                axon_infos,
                subnet_uid,
                uid,
            )
        )
    
    return related_uids


def get_related_uids_in_subnet(
    network: str,
    subnet_uid: int,
    uid: int,
) -> Dict[str, int | List[int]]:    
    bt.logging.info(f"Getting related uids in subnet {subnet_uid} for uid {uid} in network {network}")
    subtensor = bt.subtensor(network=network)
    number_of_subnets = subtensor.metagraph(0).n.item()
    ips_dict = {}
    coldkeys_dict = {}
    axon_infos = {}
    
    bt.logging.info(f"The number of subnets: {number_of_subnets}")
    bt.logging.info(f"Getting metagraph for all subnets")
    for subnet_uid in range(1, number_of_subnets + 1):
        metagraph = subtensor.metagraph(subnet_uid)
        number_of_uids = metagraph.n.item()
        for uid in range(number_of_uids):
            ip = metagraph.addresses[uid].split(":")[0]
            if ip != "0.0.0.0":
                ips_dict[ip] = ips_dict.get(ip, [])
                ips_dict[ip].append((subnet_uid, uid))
            
            coldkey = metagraph.axons[uid].coldkey
            coldkeys_dict[coldkey] = coldkeys_dict.get(coldkey, [])
            coldkeys_dict[coldkey].append((subnet_uid, uid))
            
            axon_infos[(subnet_uid, uid)] = {
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
    related_uids = [
        uid for subnet_uid, uid in related_uids_in_all_subnets if subnet_uid == subnet_uid
    ]
    
    return {
        "total_uids": len(related_uids),
        "related_uids": related_uids,
    }

if __name__ == "__main__":
    bt.logging.set_info(True)
    bt.logging.info(get_related_uids_in_subnet(network="finney", subnet_uid=54, uid=17))
