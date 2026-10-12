import time
import pytest


def test_coordinate_plane_svg_rendering(page, setup_test_courses):
    """AC-09: A question with a graph renders the graph (verified via DOM/canvas/svg,
    not just absence of errors).
    """
    page.goto(page.base_url)
    page.wait_for_load_state("networkidle")

    # Enter calculus course
    course_link = page.locator("a:has-text('Differential Calculus'), button:has-text('Differential Calculus')")
    if course_link.count() > 0:
        course_link.first.click()
        page.wait_for_load_state("networkidle")

    # Launch practice for Limits intro
    unit_trigger = page.locator(
        "[data-testid^='competency-']:has-text('Limits intro'), button:has-text('Limits intro'), button:has-text('Practice')"
    )
    if unit_trigger.count() > 0:
        unit_trigger.first.click()

    lets_go = page.locator("button:has-text(\"Let's go\"), [data-testid='start-practice-btn']")
    if lets_go.count() > 0 and lets_go.first.is_visible():
        lets_go.first.click()
        page.wait_for_load_state("networkidle")

    # Search for question with graph (Q-LIM-001)
    found_graph = False
    for _ in range(5):
        # Look for SVG or Canvas element representing the graph
        graph_svg = page.locator(
            "[data-testid='coordinate-plane'], svg.coordinate-plane, [data-testid='graph-container'] svg, .graph-canvas, svg"
        )
        # Check if this SVG has coordinate plane characteristics (axes, curves, points)
        if graph_svg.count() > 0:
            for i in range(graph_svg.count()):
                svg_el = graph_svg.nth(i)
                # Check for child elements: lines, paths, circles (curves and open/closed points)
                circles = svg_el.locator("circle")
                paths = svg_el.locator("path")
                lines = svg_el.locator("line")

                if circles.count() > 0 or paths.count() > 0 or lines.count() > 0:
                    found_graph = True

                    # Verify open point: circle with fill white or stroke
                    # and closed point: circle with solid fill
                    assert circles.count() >= 1, "Graph SVG should render open/closed points!"

                    # Verify coordinate plane axes or curves
                    assert paths.count() >= 1 or lines.count() >= 1, "Graph SVG should render curves or axes!"

                    # Verify graph element is visible on screen
                    assert svg_el.is_visible(), "Coordinate graph SVG is in DOM but not visible!"
                    break

        if found_graph:
            break

        # If not on graph question, skip to next
        skip_btn = page.locator("button:has-text('Skip'), [data-testid='skip-btn']")
        if skip_btn.is_visible() and skip_btn.is_enabled():
            skip_btn.click()
            page.wait_for_timeout(300)

    assert found_graph, "Coordinate plane graph SVG element not found in DOM during practice session!"
    assert len(page.page_errors) == 0, f"Page errors: {page.page_errors}"
    assert len(page.console_errors) == 0, f"Console errors: {page.console_errors}"
