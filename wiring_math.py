"""
RuneBox // Subwoofer Enclosure Lab
wiring_math.py - Electrical Voice Coil Synthesizer, Hybrid Topologies, Imbalance Guard & Cable Sizing
Created by NfgOdin
"""

import math
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class AmplifierSpecs:
    """Represents amplifier topology and power capability profile."""
    name: str = "Class-D Monoblock"
    topology: str = "monoblock"
    rated_rms_1ohm: float = 1200.0
    rated_rms_2ohm: float = 800.0
    rated_rms_4ohm: float = 500.0
    min_stable_impedance: float = 1.0


def calculate_wire_gauge_and_fusing(total_rms: float, final_load_ohms: float, cable_length_ft: float = 17.0, amp_efficiency: float = 0.80) -> Dict[str, Any]:
    """
    Computes professional 12V electrical recommendations:
    - 12V Primary Battery Cable AWG (OFC Copper)
    - Recommended Primary In-line Fuse (Amps ANL / Mini-ANL)
    - Subwoofer Output Speaker Wire Gauge (AWG)
    """
    # 1. 12V Current Draw at Amplifier Input: I_dc = P_rms / (V_sys * efficiency)
    v_sys = 13.8  # Standard running alternator voltage
    i_dc_peak = total_rms / (v_sys * max(0.5, amp_efficiency))

    # Standard car audio in-line ANL fuse ratings: 40, 60, 80, 100, 120, 150, 200, 250, 300, 350, 400
    fuse_ratings = [40, 60, 80, 100, 120, 150, 175, 200, 250, 300, 350, 400, 500]
    recommended_fuse = 40
    for f in fuse_ratings:
        if f >= i_dc_peak * 1.15:  # 15% headroom above RMS draw
            recommended_fuse = f
            break
    else:
        recommended_fuse = 500

    # 12V Power Cable Gauge (based on current and run length)
    if i_dc_peak <= 35:
        pwr_cable = "8 AWG OFC"
    elif i_dc_peak <= 60:
        pwr_cable = "4 AWG OFC"
    elif i_dc_peak <= 100:
        pwr_cable = "2 AWG OFC"
    elif i_dc_peak <= 175:
        pwr_cable = "1/0 AWG OFC"
    elif i_dc_peak <= 275:
        pwr_cable = "2/0 AWG or Dual 1/0 AWG"
    else:
        pwr_cable = "Dual 1/0 AWG or 4/0 AWG OFC"

    # 2. Speaker Wire Current: I_ac = sqrt(P_rms / Z_load)
    z_safe = max(0.25, final_load_ohms)
    i_speaker = math.sqrt(total_rms / z_safe)

    if i_speaker <= 10.0:
        spk_cable = "16 AWG OFC"
    elif i_speaker <= 18.0:
        spk_cable = "14 AWG OFC"
    elif i_speaker <= 28.0:
        spk_cable = "12 AWG OFC"
    elif i_speaker <= 45.0:
        spk_cable = "10 AWG OFC"
    else:
        spk_cable = "8 AWG OFC"

    return {
        "dc_current_amps": round(i_dc_peak, 1),
        "ac_speaker_amps": round(i_speaker, 1),
        "recommended_power_cable": pwr_cable,
        "recommended_fuse_amps": recommended_fuse,
        "recommended_speaker_cable": spk_cable,
        "summary": f"Power Wire: {pwr_cable} | Fuse: {recommended_fuse}A ANL | Spk Leads: {spk_cable} ({i_speaker:.1f}A RMS)"
    }


def calculate_wiring_and_amplifier_power(
    num_subs: int,
    coils_per_sub: int = 2,  # fallback if per_sub_configs not provided
    coil_ohms: float = 4.0,   # fallback
    intra_wiring: str = "parallel",  # fallback
    inter_wiring: str = "parallel",
    topology: str = "monoblock",
    amp_rated_1ohm: float = 1500.0,
    amp_rated_2ohm: float = 900.0,
    amp_rated_4ohm: float = 500.0,
    min_stable_ohm: float = 1.0,
    per_sub_configs: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Calculates driver nominal impedance, total system impedance connected to the amplifier,
    channel-specific load, power distribution per speaker, and electrical cable recommendations.
    Supports individual voice coil and impedance settings per speaker.
    """
    n_subs = max(1, num_subs)

    # 1. Calculate individual driver nominal impedance for each subwoofer
    sub_driver_z: List[float] = []
    sub_coils_list: List[int] = []
    sub_ohms_list: List[float] = []
    sub_intra_list: List[str] = []

    for i in range(n_subs):
        if per_sub_configs and i < len(per_sub_configs):
            cfg = per_sub_configs[i]
            c_count = max(1, int(cfg.get("coils", coils_per_sub)))
            r_c = max(0.25, float(cfg.get("ohms", coil_ohms)))
            i_w = str(cfg.get("intra", intra_wiring)).lower()
        else:
            c_count = max(1, coils_per_sub)
            r_c = max(0.25, coil_ohms)
            i_w = str(intra_wiring).lower()

        sub_coils_list.append(c_count)
        sub_ohms_list.append(r_c)
        sub_intra_list.append(i_w)

        if c_count == 1:
            z_drv = r_c
        elif i_w == "parallel":
            z_drv = r_c / c_count
        else:
            z_drv = r_c * c_count
        sub_driver_z.append(round(z_drv, 3))

    avg_z_driver = sum(sub_driver_z) / len(sub_driver_z)

    # Helper function to interpolate/extrapolate power curve
    def get_power_at_load(z_load: float, r1: float, r2: float, r4: float) -> float:
        if z_load <= 1.0:
            p = r1
        elif z_load <= 2.0:
            ratio = (z_load - 1.0) / (2.0 - 1.0)
            p = r1 - ratio * (r1 - r2)
        elif z_load <= 4.0:
            ratio = (z_load - 2.0) / (4.0 - 2.0)
            p = r2 - ratio * (r2 - r4)
        else:
            p = r4 * (4.0 / z_load)
        return round(max(10.0, p), 1)

    # 2. Impedance & Power calculation based on Inter-Wiring and Topology
    topo = topology.lower().strip()
    inter = inter_wiring.lower().strip()

    is_series_parallel = "series_parallel" in inter or "series-parallel" in inter or "pairs in series" in inter or "2 in series" in inter
    is_parallel_series = "parallel_series" in inter or "parallel-series" in inter or "pairs in parallel" in inter or "2 in parallel" in inter

    has_imbalance = False
    imbalance_msg = ""
    power_per_sub: List[float] = []

    # Check if subwoofers have mismatched driver impedances
    is_mixed_load = len(set(sub_driver_z)) > 1

    if "2-channel independent" in topo or "2ch_stereo" in topo or "stereo" in topo or "dual-mono" in topo:
        # 2-Channel Stereo: CH1 drives Sub 1 (and 2 if 4 subs), CH2 drives Sub 2 (and 4 if 4 subs)
        ch1_subs = [sub_driver_z[i] for i in range(0, n_subs, 2)]
        ch2_subs = [sub_driver_z[i] for i in range(1, n_subs, 2)]

        def calc_branch(subs_z):
            if not subs_z:
                return 4.0
            if len(subs_z) == 1:
                return subs_z[0]
            if inter == "series":
                return sum(subs_z)
            return 1.0 / sum(1.0 / z for z in subs_z)

        z_ch1 = calc_branch(ch1_subs)
        z_ch2 = calc_branch(ch2_subs)
        z_total = round((z_ch1 + z_ch2) / 2.0, 3)

        p_ch1 = get_power_at_load(z_ch1, amp_rated_1ohm, amp_rated_2ohm, amp_rated_4ohm)
        p_ch2 = get_power_at_load(z_ch2, amp_rated_1ohm, amp_rated_2ohm, amp_rated_4ohm) if ch2_subs else 0.0
        delivered_total_rms = p_ch1 + p_ch2
        power_per_sub_rms = round(delivered_total_rms / n_subs, 1)
        inter_desc = f"2-Channel Stereo (CH1: {z_ch1:.2f}Ω, CH2: {z_ch2:.2f}Ω)"

    elif "4-channel independent" in topo or "4ch_independent" in topo:
        ch_powers = [get_power_at_load(z, amp_rated_1ohm, amp_rated_2ohm, amp_rated_4ohm) for z in sub_driver_z]
        delivered_total_rms = sum(ch_powers)
        z_total = round(avg_z_driver, 3)
        power_per_sub_rms = round(delivered_total_rms / n_subs, 1)
        inter_desc = f"4-Channel Independent ({n_subs}x discrete channels)"

    elif "4-channel dual bridged" in topo or "dual bridged" in topo:
        # Bridge 1 drives subs 0 & 1, Bridge 2 drives subs 2 & 3
        b1_subs = sub_driver_z[:2] if n_subs >= 2 else sub_driver_z
        b2_subs = sub_driver_z[2:4] if n_subs >= 3 else []

        def calc_branch(subs_z):
            if not subs_z:
                return 4.0
            if len(subs_z) == 1:
                return subs_z[0]
            if inter == "series":
                return sum(subs_z)
            return 1.0 / sum(1.0 / z for z in subs_z)

        z_b1 = calc_branch(b1_subs)
        z_b2 = calc_branch(b2_subs) if b2_subs else z_b1
        z_total = round((z_b1 + z_b2) / 2.0, 3)

        p_b1 = get_power_at_load(z_b1, amp_rated_1ohm, amp_rated_2ohm, amp_rated_4ohm)
        p_b2 = get_power_at_load(z_b2, amp_rated_1ohm, amp_rated_2ohm, amp_rated_4ohm) if b2_subs else 0.0
        delivered_total_rms = p_b1 + p_b2
        power_per_sub_rms = round(delivered_total_rms / n_subs, 1)
        inter_desc = f"4-Ch Dual Bridged (B1: {z_b1:.2f}Ω, B2: {z_b2:.2f}Ω)"

    else:
        # Monoblock or Single Bridged Channel
        if n_subs == 1:
            z_total = sub_driver_z[0]
            inter_desc = f"Single Subwoofer ({z_total:.2f}Ω)"

        elif n_subs == 3 and is_series_parallel:
            # 3 SUBS: 2 IN SERIES, 1 IN PARALLEL
            # Branch 1 (Subs 1 & 2 in series): Z_branch1 = Z1 + Z2
            # Branch 2 (Sub 3 alone): Z_branch2 = Z3
            # Total load = 1 / (1/Z_branch1 + 1/Z_branch2)
            z_b1 = sub_driver_z[0] + sub_driver_z[1]
            z_b2 = sub_driver_z[2]
            z_total = 1.0 / ((1.0 / z_b1) + (1.0 / z_b2))

            has_imbalance = True
            imbalance_msg = f"ASYMMETRIC LOAD WARNING: Subs 1 & 2 in series ({z_b1:.2f}Ω) paralleled with Sub 3 ({z_b2:.2f}Ω). Sub 3 receives {(z_b1/(z_b1+z_b2))*100:.0f}% of total power!"
            inter_desc = f"Hybrid 3-Sub: 2 Series & 1 Parallel ({z_total:.2f}Ω)"

        elif n_subs == 3 and is_parallel_series:
            # 3 SUBS: 2 IN PARALLEL, 1 IN SERIES
            # Bank 1 (Subs 1 & 2 in parallel): Z_bank1 = 1 / (1/Z1 + 1/Z2)
            # Series with Sub 3: Z_total = Z_bank1 + Z3
            z_b1 = 1.0 / ((1.0 / sub_driver_z[0]) + (1.0 / sub_driver_z[1]))
            z_total = z_b1 + sub_driver_z[2]

            has_imbalance = True
            imbalance_msg = f"ASYMMETRIC LOAD WARNING: Subs 1 & 2 in parallel ({z_b1:.2f}Ω) in series with Sub 3 ({sub_driver_z[2]:.2f}Ω). Sub 3 carries entire circuit current!"
            inter_desc = f"Hybrid 3-Sub: 2 Parallel & 1 Series ({z_total:.2f}Ω)"

        elif n_subs == 4 and is_series_parallel:
            # Pair 1 (Subs 1 & 2 in series) in parallel with Pair 2 (Subs 3 & 4 in series)
            z_p1 = sub_driver_z[0] + sub_driver_z[1]
            z_p2 = sub_driver_z[2] + sub_driver_z[3]
            z_total = 1.0 / ((1.0 / z_p1) + (1.0 / z_p2))
            inter_desc = f"Series-Parallel (2 Series Pairs in Parallel = {z_total:.2f}Ω)"

        elif n_subs == 4 and is_parallel_series:
            # Bank 1 (Subs 1 & 2 in parallel) in series with Bank 2 (Subs 3 & 4 in parallel)
            z_b1 = 1.0 / ((1.0 / sub_driver_z[0]) + (1.0 / sub_driver_z[1]))
            z_b2 = 1.0 / ((1.0 / sub_driver_z[2]) + (1.0 / sub_driver_z[3]))
            z_total = z_b1 + z_b2
            inter_desc = f"Parallel-Series (2 Parallel Banks in Series = {z_total:.2f}Ω)"

        elif inter == "parallel":
            inv_sum = sum(1.0 / z for z in sub_driver_z)
            z_total = 1.0 / inv_sum
            inter_desc = f"{n_subs}x Subs in Parallel ({z_total:.2f}Ω)"

        else:  # series
            z_total = sum(sub_driver_z)
            inter_desc = f"{n_subs}x Subs in Series ({z_total:.2f}Ω)"

        delivered_total_rms = get_power_at_load(z_total, amp_rated_1ohm, amp_rated_2ohm, amp_rated_4ohm)

    # -------------------------------------------------------------
    # EXACT PHYSICAL POWER PER SUBWOOFER (Ohm's & Joule's Laws)
    # -------------------------------------------------------------
    sub_power_list: List[float] = [0.0] * n_subs

    if "2-channel independent" in topo or "2ch_stereo" in topo or "stereo" in topo or "dual-mono" in topo:
        ch1_indices = [i for i in range(0, n_subs, 2)]
        ch2_indices = [i for i in range(1, n_subs, 2)]
        for ch_idxs, p_ch, z_ch in [(ch1_indices, p_ch1, z_ch1), (ch2_indices, p_ch2, z_ch2)]:
            if not ch_idxs:
                continue
            if len(ch_idxs) == 1:
                sub_power_list[ch_idxs[0]] = p_ch
            elif inter == "series":
                i_sq = p_ch / max(0.1, z_ch)
                for idx in ch_idxs:
                    sub_power_list[idx] = round(i_sq * sub_driver_z[idx], 1)
            else:  # parallel
                v_sq = p_ch * z_ch
                for idx in ch_idxs:
                    sub_power_list[idx] = round(v_sq / max(0.1, sub_driver_z[idx]), 1)

    elif "4-channel independent" in topo or "4ch_independent" in topo:
        for i in range(n_subs):
            sub_power_list[i] = ch_powers[i]

    elif "4-channel dual bridged" in topo or "dual bridged" in topo:
        b1_indices = [0, 1] if n_subs >= 2 else [0]
        b2_indices = [2, 3] if n_subs >= 4 else ([2] if n_subs == 3 else [])
        for b_idxs, p_b, z_b in [(b1_indices, p_b1, z_b1), (b2_indices, p_b2, z_b2)]:
            if not b_idxs:
                continue
            if len(b_idxs) == 1:
                sub_power_list[b_idxs[0]] = p_b
            elif inter == "series":
                i_sq = p_b / max(0.1, z_b)
                for idx in b_idxs:
                    sub_power_list[idx] = round(i_sq * sub_driver_z[idx], 1)
            else:  # parallel
                v_sq = p_b * z_b
                for idx in b_idxs:
                    sub_power_list[idx] = round(v_sq / max(0.1, sub_driver_z[idx]), 1)

    else:
        # Monoblock or Single Bridged Channel (Single electrical circuit)
        if n_subs == 1:
            sub_power_list[0] = delivered_total_rms

        elif inter == "parallel":
            # In pure parallel across amplifier terminals, all drivers see identical voltage V_rms:
            # P_i = V_rms^2 / Z_i, where V_rms^2 = P_total * Z_total
            v_sq = delivered_total_rms * z_total
            for i in range(n_subs):
                sub_power_list[i] = round(v_sq / max(0.1, sub_driver_z[i]), 1)

        elif inter == "series":
            # In pure series, all drivers carry identical current I_rms:
            # P_i = I_rms^2 * Z_i, where I_rms^2 = P_total / Z_total
            i_sq = delivered_total_rms / max(0.1, z_total)
            for i in range(n_subs):
                sub_power_list[i] = round(i_sq * sub_driver_z[i], 1)

        elif n_subs == 3 and is_series_parallel:
            # Branch 1 (Subs 0 & 1 in series, Z_b1), Branch 2 (Sub 2 alone, Z_b2) in parallel
            v_sq = delivered_total_rms * z_total
            sub_power_list[0] = round(v_sq * sub_driver_z[0] / max(0.01, z_b1 ** 2), 1)
            sub_power_list[1] = round(v_sq * sub_driver_z[1] / max(0.01, z_b1 ** 2), 1)
            sub_power_list[2] = round(v_sq / max(0.1, z_b2), 1)

        elif n_subs == 3 and is_parallel_series:
            # Bank 1 (Subs 0 & 1 in parallel, Z_b1) in series with Sub 2 (Z2)
            i_sq = delivered_total_rms / max(0.1, z_total)
            v_b1_sq = i_sq * (z_b1 ** 2)
            sub_power_list[0] = round(v_b1_sq / max(0.1, sub_driver_z[0]), 1)
            sub_power_list[1] = round(v_b1_sq / max(0.1, sub_driver_z[1]), 1)
            sub_power_list[2] = round(i_sq * sub_driver_z[2], 1)

        elif n_subs == 4 and is_series_parallel:
            v_sq = delivered_total_rms * z_total
            sub_power_list[0] = round(v_sq * sub_driver_z[0] / max(0.01, z_p1 ** 2), 1)
            sub_power_list[1] = round(v_sq * sub_driver_z[1] / max(0.01, z_p1 ** 2), 1)
            sub_power_list[2] = round(v_sq * sub_driver_z[2] / max(0.01, z_p2 ** 2), 1)
            sub_power_list[3] = round(v_sq * sub_driver_z[3] / max(0.01, z_p2 ** 2), 1)

        elif n_subs == 4 and is_parallel_series:
            i_sq = delivered_total_rms / max(0.1, z_total)
            v_b1_sq = i_sq * (z_b1 ** 2)
            v_b2_sq = i_sq * (z_b2 ** 2)
            sub_power_list[0] = round(v_b1_sq / max(0.1, sub_driver_z[0]), 1)
            sub_power_list[1] = round(v_b1_sq / max(0.1, sub_driver_z[1]), 1)
            sub_power_list[2] = round(v_b2_sq / max(0.1, sub_driver_z[2]), 1)
            sub_power_list[3] = round(v_b2_sq / max(0.1, sub_driver_z[3]), 1)

        else:
            for i in range(n_subs):
                sub_power_list[i] = round(delivered_total_rms / n_subs, 1)

    power_per_sub_rms = round(sum(sub_power_list) / max(1, n_subs), 1)

    # 3. Electrical Sizing
    elec = calculate_wire_gauge_and_fusing(delivered_total_rms, z_total)

    # 4. Safety and Health Diagnostics
    power_variance = max(sub_power_list) - min(sub_power_list) if len(sub_power_list) > 1 else 0.0
    if (power_variance > 5.0 or is_mixed_load) and not has_imbalance:
        has_imbalance = True
        split_str = ", ".join([f"Sub {i+1}: {w:.0f}W ({sub_driver_z[i]:.1f}Ω)" for i, w in enumerate(sub_power_list)])
        imbalance_msg = f"ASYMMETRIC POWER DRAW: {split_str}. Lowest impedance speaker draws heaviest wattage!"

    is_unsafe = z_total < min_stable_ohm or has_imbalance
    if has_imbalance:
        status = "POWER IMBALANCE DETECTED"
        color = "#FF9100"
        diag = imbalance_msg
    elif z_total < min_stable_ohm:
        status = "CRITICAL LOAD WARNING"
        color = "#FF1744"
        diag = f"Impedance ({z_total:.2f}Ω) is BELOW amplifier minimum stable rating ({min_stable_ohm:.1f}Ω)! Risk of thermal protect / amplifier damage."
    elif z_total > 4.0:
        status = "HIGH IMPEDANCE LOAD"
        color = "#FFD600"
        diag = f"Load is {z_total:.2f}Ω. Safe and clean, but delivers less total output than low-impedance ratings."
    else:
        status = "OPTIMAL MATCH"
        color = "#00E676"
        diag = f"Safe and efficient {z_total:.2f}Ω load. Matches amplifier capabilities cleanly."

    return {
        "num_subs": n_subs,
        "sub_driver_z": sub_driver_z,
        "sub_coils_list": sub_coils_list,
        "sub_ohms_list": sub_ohms_list,
        "sub_intra_list": sub_intra_list,
        "inter_wiring": inter_wiring,
        "topology": topology,
        "z_driver_ohms": round(avg_z_driver, 3),
        "z_total_ohms": round(z_total, 3),
        "intra_desc": f"Avg Driver: {avg_z_driver:.2f}Ω",
        "inter_desc": inter_desc,
        "delivered_total_rms": delivered_total_rms,
        "power_per_sub_rms": power_per_sub_rms,
        "sub_power_list": sub_power_list,
        "is_unsafe": is_unsafe,
        "has_imbalance": has_imbalance,
        "electrical": elec,
        "status": status,
        "color": color,
        "diagnostic": diag
    }
