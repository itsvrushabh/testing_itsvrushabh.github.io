@ui @shortcuts
Feature: Global Keyboard Shortcuts
  As a power-user visiting Vrushabh's keyboard-driven website
  I want to navigate using global hotkeys
  So that I can cycle themes, open the palette, view shortcuts, and focus the TUI

  Background:
    Given I visit the website homepage

  Scenario: Cycle theme with 't' hotkey
    When I press keyboard key "t"
    Then the active theme attribute on html should change from the initial theme
    And the local storage "omarchy-site-theme" should match the active theme

  Scenario: Toggle keyboard shortcuts modal with '?'
    When I press keyboard key "?"
    Then the shortcuts modal dialog should be displayed
    When I press keyboard key "?"
    Then the shortcuts modal dialog should be closed

  Scenario: Open Command Palette with Ctrl+K and close with Escape
    When I press key combination "Control+k"
    Then the command palette dialog should be displayed
    When I press keyboard key "Escape"
    Then the command palette dialog should be closed

  Scenario: Jump to and focus interactive TUI terminal with backquote
    When I press keyboard key "`"
    Then the interactive terminal input should be focused
