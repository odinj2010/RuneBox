"""
RuneBox // Subwoofer Enclosure Lab
visualizer_3d.py - Interactive 3D Wireframe & Shaded Enclosure Visualizer.
Zero external 3D engine dependencies: uses fast 3D vector projection and depth sorting.
"""

import math
import tkinter as tk
from typing import List, Tuple, Dict, Any, Optional


class BoxVisualizer3D:
    """
    Renders an interactive 3D model of the subwoofer enclosure on a Tkinter Canvas.
    Supports real-time mouse pitch/yaw rotation, zoom, solid MDF shading with directional lighting,
    X-ray internal inspection mode, and exploded assembly view.
    """

    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas
        self.yaw = 35.0      # Horizontal rotation degrees
        self.pitch = 22.0    # Vertical tilt degrees
        self.roll = 0.0
        self.zoom = 1.0
        self.exploded_factor = 0.0  # 0.0 (assembled) to 1.0 (fully exploded)
        self.render_mode = "solid"   # "solid", "xray", "wireframe"
        self.show_internals = True
        self.show_dimensions = True

        # Mouse drag state
        self._last_mouse_x = 0
        self._last_mouse_y = 0
        self._is_dragging = False

        self._bind_events()

    def _bind_events(self):
        self.canvas.bind("<ButtonPress-1>", self._on_button_down)
        self.canvas.bind("<B1-Motion>", self._on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_button_up)
        self.canvas.bind("<MouseWheel>", self._on_mouse_wheel)  # Windows mouse wheel
        self.canvas.bind("<Button-4>", lambda e: self.adjust_zoom(1.1))  # Linux
        self.canvas.bind("<Button-5>", lambda e: self.adjust_zoom(0.9))

    def _on_button_down(self, event):
        self._last_mouse_x = event.x
        self._last_mouse_y = event.y
        self._is_dragging = True

    def _on_mouse_drag(self, event):
        if not self._is_dragging:
            return
        dx = event.x - self._last_mouse_x
        dy = event.y - self._last_mouse_y
        self._last_mouse_x = event.x
        self._last_mouse_y = event.y

        self.yaw = (self.yaw + dx * 0.7) % 360.0
        self.pitch = max(-89.0, min(89.0, self.pitch - dy * 0.7))
        self.redraw()

    def _on_button_up(self, event):
        self._is_dragging = False

    def _on_mouse_wheel(self, event):
        if event.delta > 0:
            self.adjust_zoom(1.1)
        else:
            self.adjust_zoom(0.9)

    def adjust_zoom(self, factor: float):
        self.zoom = max(0.4, min(3.0, self.zoom * factor))
        self.redraw()

    def set_view(self, view_name: str):
        if view_name == "iso":
            self.yaw = 35.0
            self.pitch = 22.0
        elif view_name == "front":
            self.yaw = 0.0
            self.pitch = 0.0
        elif view_name == "side":
            self.yaw = 90.0
            self.pitch = 0.0
        elif view_name == "top":
            self.yaw = 0.0
            self.pitch = 89.0
        elif view_name == "rear":
            self.yaw = 180.0
            self.pitch = 0.0
        self.redraw()

    def set_render_mode(self, mode: str):
        self.render_mode = mode
        self.redraw()

    def set_exploded(self, val: float):
        self.exploded_factor = max(0.0, min(1.0, val))
        self.redraw()

    # -------------------------------------------------------------
    # 3D Math & Matrix Transformation
    # -------------------------------------------------------------
    def _rotate_vertex(self, v: Tuple[float, float, float]) -> Tuple[float, float, float]:
        x, y, z = v

        # Yaw around Y axis
        rad_yaw = math.radians(self.yaw)
        cos_y = math.cos(rad_yaw)
        sin_y = math.sin(rad_yaw)
        x1 = x * cos_y + z * sin_y
        y1 = y
        z1 = -x * sin_y + z * cos_y

        # Pitch around X axis
        rad_pitch = math.radians(self.pitch)
        cos_p = math.cos(rad_pitch)
        sin_p = math.sin(rad_pitch)
        x2 = x1
        y2 = y1 * cos_p - z1 * sin_p
        z2 = y1 * sin_p + z1 * cos_p

        return (x2, y2, z2)

    def _project(self, v: Tuple[float, float, float], cw: float, ch: float, base_scale: float) -> Tuple[float, float, float]:
        """Projects 3D point to 2D screen coordinates with perspective."""
        rx, ry, rz = self._rotate_vertex(v)
        # Perspective distance
        focal_length = 65.0
        dist = focal_length + rz
        if dist < 5.0:
            dist = 5.0
        persp = (focal_length / dist) * self.zoom * base_scale

        sx = (cw / 2.0) + (rx * persp)
        # Screen Y inverted (up is negative in screen coordinates)
        sy = (ch / 2.0) - (ry * persp)
        return (sx, sy, rz)

    # -------------------------------------------------------------
    # Render Loop
    # -------------------------------------------------------------
    def redraw(self, enclosure=None, metrics=None):
        if enclosure is not None:
            self._cached_enclosure = enclosure
        if metrics is not None:
            self._cached_metrics = metrics

        enc = getattr(self, '_cached_enclosure', None)
        met = getattr(self, '_cached_metrics', None)
        if not enc:
            return

        c = self.canvas
        c.delete("all")

        cw = float(c.winfo_width())
        ch = float(c.winfo_height())
        if cw < 50 or ch < 50:
            cw = 500.0
            ch = 320.0

        # Background grid styling
        self._draw_background(c, cw, ch)

        w = enc.ext_width
        h = enc.ext_height
        d_bot = enc.ext_depth_bottom
        d_top = enc.ext_depth_top
        shape = enc.shape
        t = enc.wall_thickness
        bt = enc.baffle_thickness
        is_sealed = (getattr(enc, 'enclosure_type', 'ported') == "sealed" or enc.port_type == "none")

        # Normalize scaling
        max_dim = max(w, h, max(d_bot, d_top), 1.0)
        base_scale = min(cw, ch) * 0.45 / max_dim

        half_w = w / 2.0
        half_h = h / 2.0

        if shape == "cuboid":
            front_z = d_bot / 2.0
            rear_z = -d_bot / 2.0
            top_front_z = front_z
            top_rear_z = rear_z
            bot_front_z = front_z
            bot_rear_z = rear_z
        elif shape == "single_wedge":
            front_z = d_bot / 2.0
            bot_front_z = front_z
            top_front_z = front_z
            bot_rear_z = -d_bot / 2.0
            top_rear_z = bot_rear_z + (d_bot - d_top)
        else:  # double_wedge
            half_delta = (d_bot - d_top) / 2.0
            bot_front_z = d_bot / 2.0
            bot_rear_z = -d_bot / 2.0
            top_front_z = bot_front_z - half_delta
            top_rear_z = bot_rear_z + half_delta

        # Exploded view offsets
        exp = self.exploded_factor * (max_dim * 0.4)

        panels = []

        # 1. Front Baffle
        front_verts = [
            (-half_w, -half_h, bot_front_z + exp),
            (half_w, -half_h, bot_front_z + exp),
            (half_w, half_h, top_front_z + exp),
            (-half_w, half_h, top_front_z + exp)
        ]
        panels.append({
            "name": "Front Baffle",
            "verts": front_verts,
            "normal": (0, 0, 1),
            "color": "#3D2B1F" if self.render_mode == "solid" else None,
            "border": "#00E5FF",
            "is_baffle": True
        })

        # 2. Rear Wall
        rear_verts = [
            (half_w, -half_h, bot_rear_z - exp),
            (-half_w, -half_h, bot_rear_z - exp),
            (-half_w, half_h, top_rear_z - exp),
            (half_w, half_h, top_rear_z - exp)
        ]
        panels.append({
            "name": "Rear Wall",
            "verts": rear_verts,
            "normal": (0, 0, -1),
            "color": "#2A1E15" if self.render_mode == "solid" else None,
            "border": "#00B0FF",
            "is_baffle": False
        })

        # 3. Top Panel
        top_verts = [
            (-half_w, half_h + exp, top_front_z),
            (half_w, half_h + exp, top_front_z),
            (half_w, half_h + exp, top_rear_z),
            (-half_w, half_h + exp, top_rear_z)
        ]
        panels.append({
            "name": "Top Panel",
            "verts": top_verts,
            "normal": (0, 1, 0),
            "color": "#4A3525" if self.render_mode == "solid" else None,
            "border": "#40C4FF",
            "is_baffle": False
        })

        # 4. Bottom Panel
        bot_verts = [
            (-half_w, -half_h - exp, bot_rear_z),
            (half_w, -half_h - exp, bot_rear_z),
            (half_w, -half_h - exp, bot_front_z),
            (-half_w, -half_h - exp, bot_front_z)
        ]
        panels.append({
            "name": "Bottom Panel",
            "verts": bot_verts,
            "normal": (0, -1, 0),
            "color": "#231810" if self.render_mode == "solid" else None,
            "border": "#40C4FF",
            "is_baffle": False
        })

        # 5. Left Side Panel
        left_verts = [
            (-half_w - exp, -half_h, bot_rear_z),
            (-half_w - exp, -half_h, bot_front_z),
            (-half_w - exp, half_h, top_front_z),
            (-half_w - exp, half_h, top_rear_z)
        ]
        panels.append({
            "name": "Left Side Panel",
            "verts": left_verts,
            "normal": (-1, 0, 0),
            "color": "#332317" if self.render_mode == "solid" else None,
            "border": "#80D8FF",
            "is_baffle": False
        })

        # 6. Right Side Panel
        right_verts = [
            (half_w + exp, -half_h, bot_front_z),
            (half_w + exp, -half_h, bot_rear_z),
            (half_w + exp, half_h, top_rear_z),
            (half_w + exp, half_h, top_front_z)
        ]
        panels.append({
            "name": "Right Side Panel",
            "verts": right_verts,
            "normal": (1, 0, 0),
            "color": "#3A281B" if self.render_mode == "solid" else None,
            "border": "#80D8FF",
            "is_baffle": False
        })

        # Calculate average rotated depth (Z) for painter's algorithm sorting
        for p in panels:
            rot_verts = [self._rotate_vertex(v) for v in p["verts"]]
            avg_z = sum(v[2] for v in rot_verts) / len(rot_verts)
            p["avg_z"] = avg_z
            p["screen_coords"] = [self._project(v, cw, ch, base_scale) for v in p["verts"]]

            # Compute normal vector dot product with light source (top-front-right)
            nx, ny, nz = p["normal"]
            rnx, rny, rnz = self._rotate_vertex((nx, ny, nz))
            lx, ly, lz = (0.5, 0.7, 0.5)
            l_mag = math.sqrt(lx**2 + ly**2 + lz**2)
            lx, ly, lz = lx / l_mag, ly / l_mag, lz / l_mag
            dot = max(0.15, min(1.0, (rnx * lx + rny * ly + rnz * lz) * 0.6 + 0.4))
            p["lighting"] = dot
            p["is_facing_camera"] = (rnz > -0.05) or (self.render_mode != "solid") or (self.exploded_factor > 0.05)

        # Sort back-to-front
        panels.sort(key=lambda item: item["avg_z"])

        # Render panels
        for p in panels:
            coords_flat = []
            for sc in p["screen_coords"]:
                coords_flat.extend([sc[0], sc[1]])

            is_front_facing = p.get("is_facing_camera", True)

            if self.render_mode == "solid":
                if not is_front_facing and self.exploded_factor <= 0.05:
                    continue

                fill_col = self._apply_lighting(p["color"], p["lighting"])
                outline_col = p["border"] if is_front_facing else "#37474F"
                c.create_polygon(coords_flat, fill=fill_col, outline=outline_col, width=1.5)

            elif self.render_mode == "xray":
                stipple_pattern = "gray25" if is_front_facing else "gray12"
                c.create_polygon(coords_flat, fill="#1B2A38", outline=p["border"], width=1.5, stipple=stipple_pattern)

            else:  # Wireframe mode
                c.create_polygon(coords_flat, fill="", outline=p["border"], width=1.5)

            # If front baffle is drawn and facing camera (or in xray/wireframe), render subwoofers & port
            if p["is_baffle"] and (is_front_facing or self.render_mode != "solid"):
                self._render_baffle_features(c, enc, met, cw, ch, base_scale, half_w, half_h, bot_front_z, top_front_z, exp)

        # Internal Features (Chamber Dividers, Slot Port Channel) in X-Ray / Exploded Mode
        if (self.render_mode in ("xray", "wireframe") or self.show_internals) and not is_sealed:
            self._render_internal_port(c, enc, cw, ch, base_scale, half_w, half_h, bot_front_z, top_front_z, bot_rear_z, top_rear_z, exp)

        # Chamber divider partitions
        if enc.is_chamber_isolated and enc.num_subwoofers > 1:
            self._render_internal_dividers(c, enc, cw, ch, base_scale, half_w, half_h, bot_front_z, top_front_z, bot_rear_z, top_rear_z, exp)

        # Overlay HUD & 3D Compass / Orientation
        self._render_hud(c, cw, ch, enc, is_sealed)

    # -------------------------------------------------------------
    # Baffle Elements (Subs & Port Cutout)
    # -------------------------------------------------------------
    def _render_baffle_features(self, c, enc, met, cw, ch, base_scale, half_w, half_h, bot_front_z, top_front_z, exp):
        """Draws subwoofer cones and port opening on the 3D front baffle plane."""
        n_subs = enc.num_subwoofers
        cutout_dia = enc.sub_cutout_dia_in
        flush_dia = enc.sub_flush_dia_in
        t = enc.wall_thickness
        is_sealed = (getattr(enc, 'enclosure_type', 'ported') == "sealed" or enc.port_type == "none")

        centers = []
        if met and "sub_centers" in met:
            for (cx_in, cy_in) in met["sub_centers"]:
                bx = cx_in - half_w
                by = half_h - cy_in
                centers.append((bx, by))
        else:
            span = enc.ext_width - (2.0 * t) - (enc.port_width_in if enc.port_type == "slot" and not is_sealed else 0.0)
            gap = span / (n_subs + 1)
            for i in range(n_subs):
                bx = -half_w + t + gap * (i + 1) + (cutout_dia * i)
                centers.append((bx, 0.0))

        for idx, (bx, by) in enumerate(centers):
            y_ratio = (by + half_h) / max(0.1, (2.0 * half_h))
            bz = (bot_front_z * (1.0 - y_ratio) + top_front_z * y_ratio) + exp

            # 1. Outer Frame Flange Circle in 3D
            flange_dia = cutout_dia + 1.25
            flange_pts = self._generate_circle_3d(bx, by, bz + 0.05, flange_dia / 2.0, 16)
            sc_flange = [self._project(p, cw, ch, base_scale) for p in flange_pts]
            flange_flat = []
            for sc in sc_flange:
                flange_flat.extend([sc[0], sc[1]])
            c.create_polygon(flange_flat, fill="#121820", outline="#37474F", width=1)

            # 2. Cutout Hole Ring (Dark interior cavity)
            cutout_pts = self._generate_circle_3d(bx, by, bz + 0.1, cutout_dia / 2.0, 20)
            sc_cutout = [self._project(p, cw, ch, base_scale) for p in cutout_pts]
            cutout_flat = []
            for sc in sc_cutout:
                cutout_flat.extend([sc[0], sc[1]])
            c.create_polygon(cutout_flat, fill="#0A0D12", outline="#00E5FF", width=1.5)

            # 3. Subwoofer Dustcap & Cone in 3D
            cone_depth = -1.5 if not enc.is_inverted_sub else 1.8
            dust_pts = self._generate_circle_3d(bx, by, bz + 0.1 + cone_depth, (cutout_dia * 0.35) / 2.0, 14)
            sc_dust = [self._project(p, cw, ch, base_scale) for p in dust_pts]
            dust_flat = []
            for sc in sc_dust:
                dust_flat.extend([sc[0], sc[1]])
            dust_col = "#FF9100" if enc.is_inverted_sub else "#1B232E"
            c.create_polygon(dust_flat, fill=dust_col, outline="#546E7A", width=1)

            center_sc = self._project((bx, by, bz + 0.1), cw, ch, base_scale)
            c.create_line(center_sc[0] - 3, center_sc[1], center_sc[0] + 3, center_sc[1], fill="#80D8FF", width=1)
            c.create_line(center_sc[0], center_sc[1] - 3, center_sc[0], center_sc[1] + 3, fill="#80D8FF", width=1)

        # Slot or Round Port Opening on Baffle (if ported)
        if not is_sealed:
            if enc.port_type == "slot":
                pw = enc.port_width_in
                ph = min(enc.ext_height - 2.0 * t, enc.port_height_in)
                px_right = half_w - t
                px_left = px_right - pw
                py_bot = -half_h + t
                py_top = py_bot + ph

                z_bot = bot_front_z + exp + 0.05
                z_top = (bot_front_z * 0.1 + top_front_z * 0.9) + exp + 0.05

                port_opening = [
                    (px_left, py_bot, z_bot),
                    (px_right, py_bot, z_bot),
                    (px_right, py_top, z_top),
                    (px_left, py_top, z_top)
                ]
                sc_port = [self._project(v, cw, ch, base_scale) for v in port_opening]
                pflat = []
                for sc in sc_port:
                    pflat.extend([sc[0], sc[1]])
                c.create_polygon(pflat, fill="#0F171E", outline="#00E5FF", width=1.5)
                mid_sc = self._project(((px_left + px_right)/2, (py_bot + py_top)/2, (z_bot + z_top)/2), cw, ch, base_scale)
                c.create_text(mid_sc[0], mid_sc[1], text="PORT", fill="#80D8FF", font=("Segoe UI", 7, "bold"))
            else:
                r_dia = enc.port_dia_in
                px = half_w - t - (r_dia / 2.0) - 0.5
                py = half_h - t - (r_dia / 2.0) - 0.5
                pz = top_front_z + exp + 0.05
                round_pts = self._generate_circle_3d(px, py, pz, r_dia / 2.0, 16)
                sc_round = [self._project(p, cw, ch, base_scale) for p in round_pts]
                rflat = []
                for sc in sc_round:
                    rflat.extend([sc[0], sc[1]])
                c.create_polygon(rflat, fill="#0F171E", outline="#00E5FF", width=1.5)

    # -------------------------------------------------------------
    # Internal Port & Divider Partitions (X-Ray / Internal Render)
    # -------------------------------------------------------------
    def _render_internal_port(self, c, enc, cw, ch, base_scale, half_w, half_h, bot_front_z, top_front_z, bot_rear_z, top_rear_z, exp):
        """Draws the internal slot port divider wall and L-bend turn inside the box."""
        t = enc.wall_thickness
        bt = enc.baffle_thickness
        pw = enc.port_width_in
        p_len = enc.port_physical_length_in

        px_wall = half_w - t - pw - (enc.port_wall_thickness / 2.0)
        py_bot = -half_h + t
        py_top = half_h - t

        max_run1 = (enc.ext_depth_bottom - (bt + t)) - pw
        run1 = min(p_len, max_run1)

        p1_front_z = bot_front_z - bt
        p1_rear_z = p1_front_z - run1

        wall_verts = [
            (px_wall, py_bot, p1_front_z),
            (px_wall, py_bot, p1_rear_z),
            (px_wall, py_top, p1_rear_z),
            (px_wall, py_top, p1_front_z)
        ]
        sc_wall = [self._project(v, cw, ch, base_scale) for v in wall_verts]
        wflat = []
        for sc in sc_wall:
            wflat.extend([sc[0], sc[1]])
        c.create_polygon(wflat, fill="#1B3A4B", outline="#00E5FF", width=1.2, dash=(3, 2), stipple="gray25")

        if enc.is_l_port and p_len > max_run1:
            run2 = p_len - max_run1
            lz = bot_rear_z + t + pw
            lx_start = px_wall
            lx_end = px_wall - run2

            lbend_verts = [
                (lx_start, py_bot, lz),
                (lx_end, py_bot, lz),
                (lx_end, py_top, lz),
                (lx_start, py_top, lz)
            ]
            sc_lbend = [self._project(v, cw, ch, base_scale) for v in lbend_verts]
            lbflat = []
            for sc in sc_lbend:
                lbflat.extend([sc[0], sc[1]])
            c.create_polygon(lbflat, fill="#244E66", outline="#00E5FF", width=1.2, dash=(3, 2), stipple="gray25")

    def _render_internal_dividers(self, c, enc, cw, ch, base_scale, half_w, half_h, bot_front_z, top_front_z, bot_rear_z, top_rear_z, exp):
        """Draws partition walls between subwoofers for isolated chambers."""
        n_dividers = enc.num_subwoofers - 1
        t = enc.wall_thickness
        span = enc.ext_width - 2.0 * t
        spacing = span / enc.num_subwoofers

        for i in range(n_dividers):
            dx = -half_w + t + spacing * (i + 1)
            py_bot = -half_h + t
            py_top = half_h - t

            div_verts = [
                (dx, py_bot, bot_front_z - enc.baffle_thickness),
                (dx, py_bot, bot_rear_z + t),
                (dx, py_top, top_rear_z + t),
                (dx, py_top, top_front_z - enc.baffle_thickness)
            ]
            sc_div = [self._project(v, cw, ch, base_scale) for v in div_verts]
            dflat = []
            for sc in sc_div:
                dflat.extend([sc[0], sc[1]])
            c.create_polygon(dflat, fill="#2C3A47", outline="#40C4FF", width=1, dash=(2, 2), stipple="gray25")

    def _generate_circle_3d(self, cx: float, cy: float, cz: float, radius: float, segments: int = 16) -> List[Tuple[float, float, float]]:
        """Generates 3D points for a circle lying parallel to the front baffle plane (XY)."""
        pts = []
        for i in range(segments):
            ang = (2.0 * math.pi / segments) * i
            x = cx + radius * math.cos(ang)
            y = cy + radius * math.sin(ang)
            pts.append((x, y, cz))
        return pts

    def _apply_lighting(self, hex_color: Optional[str], factor: float) -> str:
        """Shades a hex color by the lighting normal factor."""
        if not hex_color or hex_color == "":
            return ""
        try:
            h = hex_color.lstrip('#')
            r, g, b = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
            r = int(min(255, max(15, r * factor)))
            g = int(min(255, max(15, g * factor)))
            b = int(min(255, max(15, b * factor)))
            return f"#{r:02x}{g:02x}{b:02x}"
        except Exception:
            return hex_color

    def _draw_background(self, c: tk.Canvas, cw: float, ch: float):
        """Draws subtle blueprint grid lines and ambient vignette."""
        c.create_rectangle(0, 0, cw, ch, fill="#0B0E14", outline="")
        grid_y = ch - 20
        c.create_line(15, grid_y, cw - 15, grid_y, fill="#18202A", width=1)

    def _render_hud(self, c: tk.Canvas, cw: float, ch: float, enc, is_sealed: bool):
        """Renders camera rotation angles and interactive guide overlays."""
        mode_text = f"3D View: {self.render_mode.upper()}"
        if self.exploded_factor > 0:
            mode_text += f" | Exploded: {int(self.exploded_factor * 100)}%"
        c.create_text(16, 16, text=mode_text, fill="#00E5FF", font=("Consolas", 10, "bold"), anchor="nw")

        dim_str = f"W: {enc.ext_width:.1f}\"  H: {enc.ext_height:.1f}\"  Depth: {enc.ext_depth_bottom:.1f}\""
        if enc.shape != "cuboid":
            dim_str += f" (Top: {enc.ext_depth_top:.1f}\") | Wedge: {enc.seat_recline_angle_deg:.1f}°"
        c.create_text(16, 32, text=dim_str, fill="#90A4AE", font=("Consolas", 9), anchor="nw")

        topo_label = "SEALED (ACOUSTIC SUSPENSION)" if is_sealed else f"PORTED ({enc.port_type.upper()})"
        c.create_text(16, 48, text=f"Topology: {topo_label}", fill="#80D8FF", font=("Consolas", 9), anchor="nw")

        c.create_text(16, ch - 16, text="🖱️ Click & Drag: Rotate 3D  |  Scroll Wheel: Zoom In/Out", fill="#546E7A", font=("Segoe UI", 8), anchor="sw")

        self._render_compass(c, cw - 38, 38)

    def _render_compass(self, c: tk.Canvas, cx: float, cy: float):
        """Mini 3D Orientation Gimbal in the top right corner."""
        axis_len = 22.0
        # X Axis (Red)
        rx, ry, rz = self._rotate_vertex((1.0, 0.0, 0.0))
        c.create_line(cx, cy, cx + rx * axis_len, cy - ry * axis_len, fill="#FF5252", width=2)
        c.create_text(cx + rx * (axis_len + 5), cy - ry * (axis_len + 5), text="X", fill="#FF5252", font=("Consolas", 7, "bold"))

        # Y Axis (Green)
        rx, ry, rz = self._rotate_vertex((0.0, 1.0, 0.0))
        c.create_line(cx, cy, cx + rx * axis_len, cy - ry * axis_len, fill="#00E676", width=2)
        c.create_text(cx + rx * (axis_len + 5), cy - ry * (axis_len + 5), text="Y", fill="#00E676", font=("Consolas", 7, "bold"))

        # Z Axis (Blue)
        rx, ry, rz = self._rotate_vertex((0.0, 0.0, 1.0))
        c.create_line(cx, cy, cx + rx * axis_len, cy - ry * axis_len, fill="#00B0FF", width=2)
        c.create_text(cx + rx * (axis_len + 5), cy - ry * (axis_len + 5), text="Z", fill="#00B0FF", font=("Consolas", 7, "bold"))
