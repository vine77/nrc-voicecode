;;
;; VC Mode - integration of GNU Emacs and Dragon NaturallySpeaking.
;;
;; Based on VR Mode by Barry Jaspan
;;
;; Copyright 1999 Barry Jaspan, <bjaspan@mit.edu>.  All rights reserved.
;;
;; $Id$
;;
;; This file is part of Emacs VR Mode.
;;
;; Emacs VR Mode is free software; you can redistribute it and/or modify
;; it under the terms of the GNU General Public License as published by
;; the Free Software Foundation; either version 2 of the License, or (at
;; your option) any later version.
;;
;; Emacs VR Mode is distributed in the hope that it will be useful, but
;; WITHOUT ANY WARRANTY; without even the implied warranty of
;; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
;; General Public License for more details.
;;
;; You should have received a copy of the GNU General Public License
;; along with Emacs VR Mode; if not, write to the Free Software
;; Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
;; USA

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; User options
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defvar vr-command "vr.exe" "*The \"vr.exe\" program to be
invoked as the VR mode sub-process.  This can be just the name, if the
program is in your PATH, or it can be a full path.")

(defvar vr-host nil "*The name of the computer running the VR Mode
process.  If nil, the process will be started on this computer.  See
also vr-port.")
(setq vr-host ""127.0.0.1"")

(defvar vr-port 0 "*The port on which to connect to vr-host.  If
vr-host is nil, this can be zero to tell the VR Mode process to use
any available port.")
(setq vr-port 45770)

(defvar vr-sr-server-assumes-verbatim-dict nil

  "If true, then the speech server assumes that user utterances are
typed verbatim into the buffers. Therefore we need to implement a
number of hacks to \"fix\" the speech server's change map (i.e. map of
which text corresponds to which text).

If false, then the speech server assumes that Emacs will tell it what was typed
as a response to a particular utterance, and that the server will maintain
its change map appropriately."  
)

(defvar vr-win-class nil
  "*Class name of the Windows window for which VR Mode will accept
voice input.  Whenever a window matching vr-win-class and vr-win-title
(which see) is the foreground window, dictation and commands spoken
into the microphone will be executed by VR Mode.")
(defvar vr-win-title "emacs"
  "*Title of the Windows window for which VR Mode will accept voice
input.  Whenever a window matching vr-win-class (which see) and
vr-win-title is the foreground window, dictation and commands spoken
into the microphone will be executed by VR Mode.")

(defvar vr-activation-list nil
  "*A list of buffer name patterns which VR Mode will voice activate.
Each element of the list is a REGEXP.  Any buffer whose name matches
any element of the list is voice activated.  For example, with

(setq vr-activation-list '(\"^\\*scratch\\*$\" \"\\.txt$\"))

the buffer named \"*scratch*\" and any buffer whose name ends with
\".txt\" will be voice-activated.  Note that voice activation of the
minibuffer is controlled by vr-activate-minibuffer.")

(defvar vr-activate-minibuffer t
  "*Flag controlling whether the minibuffer is voice-activated.")

(defvar vr-voice-command-list '(vr-default-voice-commands)
  "*The list of Emacs interactive commands that can be invoked by
voice.  Each element can be a command, a CONS cell containing
spoken text and a command or key sequence, or the special symbol
'vr-default-voice-commands, which implicitly includes the voice
commands in vr-default-voice-command-list (which see).

For example:

(setq vr-voice-command-list
      '(vr-default-voice-commands
	my-command
	(\"other command\" . my-other-command)
	(\"prefix shell command\" . [\?\\C-u \?\\M-\\S-!])))

sets up the voice commands

	Spoken			Invokes
	===============		=============
	my command		M-x my-command
	other command		M-x my-other-command
	prefix shell command	C-u M-S-! (i.e. C-u M-x shell-command)

along with all the commands on vr-default-voice-command-list.")

(defconst vr-default-voice-command-list
  '(

    ;; Lists
    (list "0to20" "0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20")
    
    ;; VR Mode commands
    ("activate buffer" . vr-add-to-activation-list)

    ;; general emacs commands
    ("quit" . [?\C-g])
    ("undo" . undo)
    ("undo that" . undo)

    ;; keystrokes that often should not be self-inserted
    ("enter" . [?\C-j])
    ("tab" . [?\C-i])
    ("space" . [? ])

    ;; Repeat control commands.  These must be invoked with funcall, not M-x,
    ;; since M-x (or any non-RET event) terminates the repeat.
    ("faster" . "vr-repeat-mult-rate 0.5")
    ("slower" . "vr-repeat-mult-rate 2")
    ("stop" . "vr-repeat-stop nil")

    ;; Repeat that.
    ("repeat that <0to20> times" . vr-repeat-that)

    ;; files
    find-file
    save-buffer
    ("save file" . save-buffer)
    find-file-other-window
    find-file-other-frame
    
    ;; buffers
    switch-to-buffer
    kill-buffer
    switch-to-buffer-other-window
    switch-to-buffer-other-frame
    ("resynchronize" .  vr-resynchronize)
    
    ;; windows
    ("split window" . split-window-vertically)
    other-window
    delete-window
    delete-other-windows
    
    ;; frames
    
    ;; cursor movement
    ("forward char <0to20>" . forward-char) 
    ("backward char <0to20>" . backward-char )
    ("forward word <0to20>" . forward-word)
    ("backward word <0to20>" . backward-word)
    ("next line <0to20>" . next-line)
    ("previous line <0to20>" . previous-line)
    ("forward paragraph <0to20>" . forward-paragraph)
    ("backward paragraph <0to20>" . backward-paragraph)
    ("scroll up" . scroll-up)
    ("scroll down" . scroll-down)
    ("page down" . scroll-up)
    ("page up" . scroll-down)
    ("beginning of line" . beginning-of-line)
    ("end of line" . end-of-line)
    ("beginning of buffer" . beginning-of-buffer)
    ("end of buffer" . end-of-buffer)

    ("move up" . vr-repeat-move-up-s)
    ("move up slow" . vr-repeat-move-up-s)
    ("move up fast" . vr-repeat-move-up-f)
    ("move down" . vr-repeat-move-down-s)
    ("move down slow" . vr-repeat-move-down-s)
    ("move down fast" . vr-repeat-move-down-f)
    ("move left" . vr-repeat-move-left-s)
    ("move left slow" . vr-repeat-move-left-s)
    ("move left fast" . vr-repeat-move-left-f)
    ("move right" . vr-repeat-move-right-s)
    ("move right slow" . vr-repeat-move-right-s)
    ("move right fast" . vr-repeat-move-right-f)

    ("move up <0to20>" . previous-line)
    ("move down <0to20>" . next-line)
    ("move left <0to20>" . backward-char)
    ("move right <0to20>" . forward-char)
    ("move left <0to20> words" . backward-word)
    ("move right <0to20> words" . forward-word)
    ("move left <0to20> sentences" . backward-sentence)
    ("move right <0to20> sentences" . forward-sentence)
    ("move left <0to20> paragraphs" . backward-paragraph)
    ("move right <0to20> paragraphs" . forward-paragraph)
    ("back <0to20>" . backward-char)
    ("forward <0to20>" . forward-char)
    ("back <0to20> words" . backward-word)
    ("forward <0to20> words" . forward-word)
    ("back <0to20> sentences" . backward-sentence)
    ("forward <0to20> sentences" . forward-sentence)
    ("back <0to20> paragraphs" . backward-paragraph)
    ("forward <0to20> paragraphs" . forward-paragraph)

    ;; deleting text
    ("delete char <0to20>" . delete-char)
    ("kill word <0to20>" . kill-word)
    ("backward kill word <0to20>" . backward-kill-word)
    ("kill line <0to20>" . kill-line)
    ("repeat kill line" . "vr-repeat-kill-line 0.5")
    yank
    yank-pop
    ;; assumes yank-pop has key binding, else last-command==self-insert-command
    ("yank again" . yank-pop)
    ;; requires a key binding for yank, repeat yank to work!
    ("repeat yank" . vr-repeat-yank)

    ;; Searching
    ("I search forward" . isearch-forward)
    ("I search backward" . isearch-backward)
    ("repeat I search forward" . vr-repeat-search-forward-s)
    ("repeat I search backward" . vr-repeat-search-backward-s)

    ;; formatting
    fill-paragraph
    
    ;; modes
    auto-fill-mode
    exit-minibuffer
    )
  "*A list of standard Emacs voice commands.  This list is used as-is
whenever vr-voice-command-list (which see) includes the symbol
'vr-default-voice-commands, or it can be appended explicitly in a
custom vr-voice-command-list.")

(defvar vr-log-do nil "*If non-nil, VR mode prints debugging information
in the 'vr-log-buff-name buffer.")
(setq vr-log-do t)

(defvar vr-log-send nil "*If non-nil, VR mode logs all data sent to the VR
subprocess in the 'vr-log-buff-name buffer.")

(defvar vr-log-read nil "*If non-nil, VR mode logs all data received
from the VR subprocess in the 'vr-log-buff-name buffer.")

(defvar vr-log-buff-name "*vr*" "Name of the buffer where VR log messages are 
sent."
)
(setq vr-log-buff-name "*Messages*")
(setq message-log-max 100000)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Configuration hooks
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defvar vr-mode-setup-hook nil
  "Hooks that are run after VR Mode is enabled but before VR.EXE is
successfully started (or connected to).  See also
vr-mode-startup-hook, called later.")

(defvar vr-mode-cleanup-hook nil
  "Hooks that are run after VR Mode is disabled and after VR.EXE has
exited or been told to exit.")

(defvar vr-mode-startup-hook nil
  "Hooks that are run after VR Mode is enabled, VR.EXE is
successfully started (or connected to), and after VR.EXE is initialized
with any per-connection state such as voice commands.  See also
vr-mode-setup-hook, called earlier.")

(defvar vr-mode-modified-hook nil
  "Hooks that are called whenever a voice activated buffer is modifed
for any reason, invoked by the 'modified-hooks property of vr-overlay.
Arguments provided are OVERLAY AFTER BEG END LEN.  If any hook returns
non-nil, VR Mode will *not* perform its normal modification processing
(ie: telling VR.EXE/DNS about the change).

If vr-changes-caused-by-sr-cmd is not nil, the hook has been invoked inside
vr-cmd-make-changes, which means the current change comes from DNS,
not from the keyboard or elsewhere.

Danger, Will Robinson!")


(defvar vr-wait-for-handshake-hook nil
   "This hook is invoked after opening a first network connection to the
speech server. It should wait until Emacs has shaken hands with the speech
server on that first connection."
)

(defvar vr-deserialize-message-hook nil
   "This hook is used to deserialize a string message (received from the speech server) into a Lisp data structure."
)

(defvar vr-serialize-message-hook nil
  "This hook is used to serialize a Lisp data structure into a string 
message that can be sent to the speech server."
)

(defvar vr-serialize-changes-hook nil
  "This hook is used to serialize a list of changes to a buffer as a string
message that can be sent to the speech server"
)

(defvar vr-send-activate-buffer-hook nil
  "This hook is used to tell the speech server that Emacs wants a particular
buffer to be speech enabled"
)

(defvar vr-send-deactivate-buffer-hook nil
  "This hook is used to tell the speech server that Emacs wants a particular
buffer to be speech disabled"
)


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Internal variables
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defvar vr-mode nil
  "Non-nil turns on VR (Voice Recognition) mode.  DO NOT SET THIS
VARIABLE DIRECTLY.  Call M-x vr-mode instead.")

(defvar vr-internal-activation-list nil
  "The working copy of vr-activation-list.  Keeping it separate allows
re-starting VR Mode to undo vr-add-to-activation-list.")

(defvar vr-mode-line " VR"
  "String displayed in the minor mode list when VR mode is enabled.
In the dictation buffer, the format is VR:<micstate>.")
(make-variable-buffer-local 'vr-mode-line)
(if (not (assq 'vr-mode minor-mode-alist))
    (setq minor-mode-alist (cons '(vr-mode vr-mode-line)
				 minor-mode-alist)))

(defvar vr-mic-state "not connected"
  "String storing the microphone state for display in the mode line.")

(defvar vr-overlay nil
  "Overlay used to track changes to voice-activated buffers.")
(make-variable-buffer-local 'vr-overlay)

(defvar vr-select-overlay (make-overlay 1 1)
  "Overlay used to track and visually indicate the NaturallySpeaking
selection.")
(delete-overlay vr-select-overlay)
(overlay-put vr-select-overlay 'face 'region)
(if (eq window-system nil)
    (progn
      (overlay-put vr-select-overlay 'before-string "[")
      (overlay-put vr-select-overlay 'after-string "]")))

(defvar vr-process nil "The VR mode subprocess.")
(defvar vr-emacs-cmds nil)
(defvar vr-dns-cmds nil)

(defvar vr-reading-string nil "Storage for partially-read commands
from the VR subprocess.")

(defvar vr-buffer nil "The current voice-activated buffer, or nil.
See vr-activate-buffer and vr-switch-to-buffer.")

(defvar vr-ignore-changes nil "see comment in vr-overlay-modified")
(defvar vr-changes-caused-by-sr-cmd nil "see comment in vr-overlay-modified")
(defvar vr-queued-changes nil "see comment in vr-overlay-modified")
(defvar vr-dont-report-sr-own-changes t 
  "If t, then we don't report the changes that have been caused directly
by the SR. However, we do report changes done automatically by Emacs
in response to a change done by the SR (e.g. auto-fill).")

(defvar vr-cmd-executing nil
  "If non-nil, the command symbol heard by NaturallySpeaking and
currently being executed by VR Mode, for which VR.EXE is expecting a
reply when done.")

(defvar vr-resynchronize-buffer nil)
(make-variable-buffer-local 'vr-resynchronize-buffer)

;; all of these variables have to do with abbreviation expansion functions
(defvar deferred-function nil)
(defvar vr-deferred-deferred-function nil)
(defvar vr-deferred-deferred-deferred-function nil)
;; this is necessary if people aren't using the abbreviation functions
(if (not (boundp 'fix-else-abbrev-expansion))
    (defun fix-else-abbrev-expansion () nil))

;(define-hash-table-test 'string= 'string= 'sxhash)
(defvar vr-message-handler-hooks (make-hash-table :test 'string=)
  "This hash table associates command names with functions used to 
process the command."
)

(defconst vr-nonlocal-exit-commands
  '(exit-minibuffer minibuffer-complete-and-exit)
  "These commands never exit and can't be executed in the make-changes
loop without screwing up the I/O.") 


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Fixes for miscellaneous interaction issues
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; for some reason activating a buffer in VR mode sometimes makes this
;; function fail to substitute every character in the region, which in
;; turn makes fill-paragraph end up in an infinite loop.  The "fix"
;; for this is to search the region after the command has completed,
;; and rerun it if it didn't work correctly.  It would be better to
;; figure out why it happens in the first place, but I have no idea.
(defadvice subst-char-in-region (after fix-mysterious-substitution-bug activate
				       compile )
  "make sure that the substitution worked"
  (save-excursion
    (save-restriction
      (narrow-to-region start end)
      (goto-char start)
      (if (search-forward (char-to-string fromchar) nil t)
	  ;; failed, retry
	  (progn
	    (message "advice redoing substitution")
	    (subst-char-in-region start end fromchar tochar noundo))
	))))

;; when else-mode expands a placeholder, the buffer frequently gets
;; out of sync.  We advise the piece of function that does this, and
;; ask for a manual resynchronization.
(defadvice else-replicate-placeholder-string (after
					      resynchronize-it
					      activate compile)
  "make VR mode resynchronize the buffer after a placeholder has been
expanded, since they often make it go out of sync."

  (message "Resynchronizing VR-buffer")
  (call-interactively 'vr-resynchronize)
  )

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Key bindings
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defvar vr-prefix-map nil "Prefix key used to access VR mode commands.")
(defvar vr-map nil)
(if vr-map
    nil
  (setq vr-map (make-sparse-keymap))
  (define-key vr-map "ws" 'vr-show-window)
  (define-key vr-map "wh" 'vr-hide-window)
  (define-key vr-map "B" 'vr-add-to-activation-list)
  (define-key vr-map "b" 'vr-switch-to-buffer)
  (define-key vr-map "m" 'vr-toggle-mic)
  (define-key vr-map "q" 'vr-quit)
  (define-key vr-map "\C-\M-y" 'vr-repeat-yank)
  )

(if vr-prefix-map
    nil
  (setq vr-prefix-map (make-sparse-keymap))
  (define-key vr-prefix-map "\C-cv" vr-map))

(if (not (assq 'vr-mode minor-mode-map-alist))
    (setq minor-mode-map-alist
	  (cons (cons 'vr-mode vr-prefix-map) minor-mode-map-alist)))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Entry points for global hooks
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defun vr-enter-minibuffer ()
  (if (and vr-emacs-cmds vr-activate-minibuffer)
      (vr-activate-buffer (current-buffer))))

(defun vr-post-command ()
  (add-hook 'post-command-hook 'vr-post-command)
  (if (overlayp vr-select-overlay)
      (delete-overlay vr-select-overlay))
  (vr-log (format "post-command: %s %s %s\n" this-command
	  vr-cmd-executing (buffer-name)))
  (if vr-emacs-cmds
      (progn
	(vr-maybe-activate-buffer (current-buffer))
	(if (and vr-cmd-executing t) ;  (eq vr-cmd-executing this-command))
; apparently this-command is not always set to the name of the
; command, for example kill-line is executed with "kill-region" in
; this-command, so this check doesn't really work
	    (progn
	      (vr-send-cmd (format "command-done %s" vr-cmd-executing))
	      (setq vr-cmd-executing nil)))
	)))

(defun vr-kill-buffer ()
  (vr-log "-- vr-kill-buffer: invoked, (current-buffer)=%S" 
		  (current-buffer))
  (if (vr-activate-buffer-p (current-buffer))
      (progn
	(vr-log (format "kill-buffer: %s\n" (current-buffer)))
	(run-hooks 'vr-send-kill-buffer-hook)
	)
    )
  (vr-log "-- vr-kill-buffer: exiting\n")
)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Buffer activation control
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defun vr-filter (pred in)
  (let (out el)
    (while in
      (setq el (car in))
      (setq in (cdr in))
      (if (funcall pred el)
	  (setq out (cons el out)))
      )
out))
  
(defun vr-add-to-activation-list (buffer)
  "Adds BUFFER, which can be a buffer name or buffer, to the list of
buffers that are voice activated.  Called interactively, adds the
current buffer.

The only way to undo the effect of this function is to re-start VR
Mode."
  ;; If called interactively, vr-post-command will activate the
  ;; current buffer (so this function doesn't have to).
  (interactive (list (current-buffer)))
  (if (bufferp buffer)
      (setq buffer (buffer-name buffer)))
  (if (vr-activate-buffer-p buffer)
      nil
    (setq vr-internal-activation-list
	  (cons (concat "^" (regexp-quote buffer) "$")
		vr-internal-activation-list))))

(defun vr-resynchronize (buffer)
  "asks VR mode to resynchronize this buffer, if it has gotten out of
sync.  (That shouldn't happen, in an ideal world, but..."
  (interactive (list (current-buffer)))
  (set-buffer buffer)
  (setq vr-resynchronize-buffer t))

(defun vr-activate-buffer-p (buffer)
  "Predicate indicating whether BUFFER matches any REGEXP element and
does not match any '(not REGEXP) element of
vr-internal-activation-list.  BUFFER can be a buffer or a buffer name."
  (vr-log "**-- vr-activate-buffer-p: buffer=%S, vr-activation-list=%S, vr-internal-activation-list=%S\n" buffer vr-activation-list vr-internal-activation-list)
  (if (bufferp buffer)
      (setq buffer (buffer-name buffer)))
  (if (string-match "^ \\*Minibuf-[0-9]+\\*$" buffer)
      vr-activate-minibuffer
    (and (vr-filter (lambda (r) (and (stringp r) (string-match r buffer)))
		    vr-internal-activation-list)
	 (not (vr-filter (lambda (r) 
			   (and (consp r) (eq (car r) 'not)
				(string-match (car (cdr r)) buffer)))
			 vr-internal-activation-list)))))

(defun vr-maybe-activate-buffer (buffer)
  ;; Deactivate whenever isearch mode is active.  This is a
  ;; "temporary" solution until isearch mode can be supported.
  (if (and (not isearch-mode) (vr-activate-buffer-p (buffer-name buffer)))
      (if (eq buffer vr-buffer)
	  nil
	(vr-activate-buffer buffer))
    (if vr-buffer 
	(vr-activate-buffer nil))))

(defun vr-switch-to-buffer ()
  "Select the current VR mode target buffer in the current window."
  (interactive)
  (if (buffer-live-p vr-buffer)
      (switch-to-buffer vr-buffer)
    (error "VR target buffer no longer exists; use vr-activate-buffer")))

(defun vr-activate-buffer (buffer)
  "Sets the target BUFFER that will receive voice-recognized text.  Called
interactively, sets the current buffer as the target buffer."
  (interactive (list (current-buffer)))
  (if (buffer-live-p vr-buffer)
      (save-excursion
	(set-buffer vr-buffer)
	;; somehow vr-buffer can be set to the minibuffer while
	;; vr-overlay is nil.
	(if (overlayp vr-overlay)
	    (delete-overlay vr-overlay))
	(setq vr-overlay nil)
	(kill-local-variable 'vr-mode-line)))
  (set-default 'vr-mode-line (concat " VR-" vr-mic-state))
  (setq vr-buffer buffer)
  (if buffer
      (save-excursion
	(set-buffer buffer)
	(setq vr-mode-line (concat " VR:" vr-mic-state))
	(run-hooks 'vr-send-activate-buffer)
	(if vr-overlay
	    nil
	  (setq vr-modification-stack ())
	  (setq vr-overlay-before-count 0)
	  (setq vr-overlay (make-overlay (point-min) (point-max) nil nil t))
	  (overlay-put vr-overlay 'modification-hooks '(vr-overlay-modified))
	  (overlay-put vr-overlay 'insert-in-front-hooks '(vr-grow-overlay))
	  (overlay-put vr-overlay 'insert-behind-hooks '(vr-grow-overlay)))
	)
    (run-hooks 'vr-send-deactivate-buffer)
    )
  (force-mode-line-update)
  )

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Tracking changes to voice-activated buffers
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defvar vr-overlay-before-count 0 "see comment in vr-grow-overlay")

(defun vr-grow-overlay (overlay after beg end &optional len)
  ;; Make OVERLAY grow to contain range START to END.  If called "before"
  ;; twice before called "after", only call vr-overlay-modified once.
  ;; This happens when we type the first char in the buffer, because I
  ;; guess it is inserted both before and after the empty overlay.

  (vr-log "Grow: %s %d %d %s %d\n" (if after "After: " "Before: ") beg end
  	  (if after (int-to-string len) "") vr-overlay-before-count)
  (if after
      (progn
	(move-overlay overlay
		      (min beg (overlay-start overlay))
		      (max end (overlay-end overlay)))
	(setq vr-overlay-before-count (1- vr-overlay-before-count))
	(if (> vr-overlay-before-count 0)
	    (progn;; (vr-log "   ignored duplicate grow\n")
	      nil)
	  (vr-report-change overlay after beg end len))
	;;(setq vr-modification-stack (cdr vr-modification-stack))
	)

    (setq vr-overlay-before-count (1+ vr-overlay-before-count))
    ;;(setq vr-modification-stack (cons (buffer-substring beg end)
    ;;vr-modification-stack))
    )
  (vr-log "-- vr-grow-overlay: exited\n")
  )

(defvar vr-modification-stack () )

(defun vr-overlay-modified (overlay after beg end &optional len)
  (vr-log " overlay modified: a:%s vro:%s %d %d %d: \"%s\"\n"
	  after (eq vr-overlay overlay) beg end (if after len 0)
	  (buffer-substring beg end))
  (vr-log "  modification stack: %d\n" (length vr-modification-stack))
  (if after
      (progn
	(vr-log "   %s %s \n" (car vr-modification-stack)
		(buffer-substring beg end))
	(if (equal (car vr-modification-stack) (buffer-substring beg end))
	    ;; the before and after text are the same, so so it's one of these
	    ;; funky changes we can ignore.
	    (vr-log "ignoring bogus change\n" );;nil
	  ;; they're not equal, so we call the modification routine like before.
	  (vr-report-change overlay after beg end len))
	(setq vr-modification-stack (cdr vr-modification-stack))
	(if (< 0 vr-overlay-before-count)
	    (setq vr-overlay-before-count (1- vr-overlay-before-count))))

    ;; for the before call, we just save the prechange string in the stack
    (setq vr-modification-stack (cons (buffer-substring beg end)
				      vr-modification-stack)))

  (vr-log "-- vr-overlay-modified: exited\n")

  )

(defun vr-change-is-delete (beg end &optional len)
  (and (> len 0) (eq beg end))
)

(defun vr-change-is-self-insert (beg end &optional len)
  (and (eq len 0) 
       (eq (- end beg) 1) 
       (eq (char-after beg) last-command-char))
)

(defun vr-report-change (overlay after beg end &optional len)
  (vr-log "-- vr-report-change: invoked\n")
  (if (and (not (run-hook-with-args-until-success 'vr-mode-modified-hook
						  overlay after beg end len))
	   after)
      ;;
      ;; If 'vr-changes-caused-by-sr-cmd not nil, the changes have
      ;; been generated by a command from the SR server. The value of
      ;; 'vr-changes-caused-by-sr-cmd is the name of that command.
      ;;
      ;; In such cases, 'vr-ignore-changes specifies a type
      ;; of change that should be ignored altogether. All other changes 
      ;; are put in a queue instead of being sent right away, to avoid
      ;; synchronization problems.  make-changes will send them when
      ;; it is done. 
      ;;
      ;; This is not a foolproof heuristic.
      (progn
	(vr-log "**-- vr-report-change: inside 1st if\n")
	(vr-log "**-- vr-report-change: vr-ignore-changes=%S, vr-changes-caused-by-sr-cmd=%S\n" 
		vr-ignore-changes vr-changes-caused-by-sr-cmd)

;;	(vr-log " overlay modified: a:%s vro:%s %d %d %d: \"%s\"\n"
;;		after (eq vr-overlay overlay) beg end len
;;		(buffer-substring beg end))
	(if (or (and (eq vr-ignore-changes 'self-insert)
		     (vr-change-is-self-insert beg end len))
		(and (eq vr-ignore-changes 'delete)
		     (vr-change-is-delete beg end len)))
	    (progn (vr-log "ignore: %d %d %d: \"%s\" %s\n" beg end len
			   (buffer-substring beg end) vr-ignore-changes)
		   nil)

	(vr-log "**-- vr-report-change: NOT ignoring changes\n")

;	  (vr-log " After: %s %d %d %d: \"%s\"\n" overlay beg end len
;		  (buffer-substring beg end))
	  (let ((the-change nil) (cmd nil))
	    (setq the-change (list 
			      (buffer-name (overlay-buffer overlay))
			      (1- beg) (1- end) len
			      (buffer-modified-tick)
			      (buffer-substring beg end)))

	(vr-log (format "**-- vr-report-change: the-change=%S\n" the-change))

	    (if vr-changes-caused-by-sr-cmd
	        (setq vr-queued-changes (cons the-change vr-queued-changes))
	      (vr-log "**-- vr-report-change: sending the changes\n")
	      (run-hook-with-args 
	        'vr-send-cmd
		(run-hook-with-args  
		  'vr-serialize-changes-hook nil (list the-change)))))))
	      
    (vr-log " overlay modified: a:%s vro:%s %d %d : \"%s\"\n"
	    after (eq vr-overlay overlay) beg end 
	    (buffer-substring beg end))
    )

  (vr-log "**-- vr-report-change: before deferred-function\n")

  (if deferred-function
      (progn
	(setq vr-deferred-deferred-function deferred-function)
	(setq deferred-function nil)
	;(debug)
	(delete-backward-char 2)
	;(debug)
	(fix-else-abbrev-expansion)
	;(debug)
	(if (not (eq vr-deferred-deferred-function
		     'else-expand-placeholder))
	    (progn
	      ;;(call-interactively deferred-deferred-function)
	      (vr-log "report-change executing deferred function %s\n" vr-deferred-deferred-function)
	      (setq vr-deferred-deferred-deferred-function
		    vr-deferred-deferred-function )
	      (setq vr-deferred-deferred-function nil)
	      (vr-execute-command
	       vr-deferred-deferred-deferred-function))
	  (vr-log "report-change deferring command %s\n"
		  vr-deferred-deferred-function))
    ))

  (vr-log "-- vr-report-change: exited\n")
  
  t  )


(defun vr-string-replace (src regexp repl)
  (let ((i 0))
    (while (setq i (string-match regexp src))
      (setq src (concat (substring src 0 i)
			repl
			(substring src (match-end 0))))
      (setq i (match-end 0))))
  src)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Keyboard lockout during voice recognition
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defvar vr-recognizing nil)

(defun vr-sleep-while-recognizing ()
  (interactive)
  (let* ((first t) (count 0))
    (while (and (< count 200) vr-recognizing (string= vr-mic-state "on"))
      (if first (message "Waiting for voice recognition..."))
      (setq first nil)
      (setq count (1+ count))
      (sleep-for 0 50))
    (if (eq count 200) 
	(message "Time out in vr-sleep-while-recognizing!")
      (message nil))))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Subprocess communication.
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defun vr-log (&rest s)
  (if vr-log-do
      (let* (
	     (buf (get-buffer-create vr-log-buff-name))
	     (win (get-buffer-window buf 't))
	     )
	(save-excursion
	  (set-buffer buf)
	  (goto-char (point-max))

 	  ;;;
	  ;;; If (length s) > 1, first argument is a format string, and the 
	  ;;; other arguments are objects to be formatted into that string.
	  ;;;
	  ;;; If (length s) == 1, its single element is a string that's
	  ;;; not meant to be used as a format string. Just insert it as
	  ;;; is instead of formatting it, because it might just happen to 
	  ;;; contain some format descriptions (e.g. %s), in which case
	  ;;; formatting it would cause "not enough arguments" error.
	  ;;;
;	  (message (format "**-- vr-log: (length s)=%S" (length s)))
	  (if (= 1 (length s))
	      (insert (nth 0 s))
	    (insert (apply 'format s))
	    )
	  (if win
	      (set-window-point win (point-max)))
	  )))
  t
)

(defun vr-sentinel (p s)
  (if (equal s "finished\n")
      (progn
	(if (processp vr-process)
	    (delete-process vr-process))
	(if (processp vr-emacs-cmds)
	    (delete-process vr-emacs-cmds))
	(if (processp vr-dns-cmds)
	    (delete-process vr-dns-cmds))
	(setq vr-process nil
	      vr-emacs-cmds nil
	      vr-dns-cmds nil))
    (error "VR process exited with status \"%s\"" s)))




;; executes a command, and runs the appropriate hooks.  It's used by
;; heard-command and by the deferred-function executions.  VR-command
;; can either be a symbol or a list.
(defun vr-execute-command (vr-command)
  (let ((cmd (or (and (listp vr-command ) (car vr-command))
		 vr-command)))
	  (run-hooks 'pre-command-hook)
 	  (condition-case err
	      (if (and (listp vr-command) 
		       (> (length vr-command) 1))
		  (apply cmd (cdr vr-command))
		(call-interactively cmd))
	    ('wrong-number-of-arguments
	     (ding)
	     (message
	      "VR Mode: Wrong number of arguments calling %s"
	      vr-command))
	    ('wrong-type-argument 'error
				  (ding)
				  (message "VR Mode: %s calling %s"
					   (error-message-string err)
					   vr-command )))
	  (vr-log "running post-command-hook for %s\n" cmd)
 	  (let ((this-command cmd))
	    (run-hooks 'post-command-hook)))
  t)


(defun vr-send-queued-changes (vr-request)
  "Send changes that were queued as a result of VR.exe request 
'vr-request"
	(vr-log "sending tick\n")
	(vr-send-reply (buffer-modified-tick))
	(vr-send-reply (length vr-queued-changes))
	(mapcar 'vr-send-reply (nreverse vr-queued-changes))
)

(defun vr-execute-event-handler (handler vr-request)

  (let ((vr-changes-caused-by-sr-cmd vr-cmd))
    (vr-log "**-- vr-execute-event-handler: debug-on-error=%S" debug-on-error)
    (if debug-on-error
	;;;
	;;; If in debug mode, let the debugger intercept errors.
	;;;
	(apply handler (list vr-request))

      ;;; 
      ;;; Not debug mode. We intercept errors ourself.
      ;;;
      (condition-case err
	  (apply handler (list vr-request))
	('error 
	 (progn
	   (message (format "Error executing VR request %s"
				       vr-request))
	   (run-hook-with-args 'vr-upon-cmd-error vr-request)
	   )
	 )
	)
      )
    )
)

		
(defun vr-output-filter (p s)
  (vr-log "**-- vr-output-filter: invoked\n")
  (setq vr-reading-string (concat vr-reading-string s))
;  (vr-log (format "**-- vr-output-filter: after concatenation, vr-reading-string=%s\n" vr-reading-string))
  (while (> (length vr-reading-string) 0)
;    (vr-log "**-- vr-output-filter: inside while, vr-deserialize-message-hook=%S\n" vr-deserialize-message-hook)
    (let* ((handler) 
	   (parsed (condition-case err
 		       (run-hook-with-args 
			   'vr-deserialize-message-hook vr-reading-string)
		     ('end-of-file (error "Invalid VR command received: %s"
					  vr-reading-string))))
;	   (vr-log (format "**-- vr-output-filter: parsed=%S" parsed))
	   (vr-request (elt parsed 0))
	   (idx (elt parsed 1))
	   (vr-cmd (elt vr-request 0)))
;	   (vr-log "**-- vr-output-filter: idx=%S, vr-cmd=%S, vr-request=%S\n"  idx vr-cmd vr-request)
      (if vr-log-read
	  (vr-log "-> %s\n" (substring vr-reading-string 0 idx)))
      (setq vr-reading-string 
	    (if (< idx (1- (length vr-reading-string)))
		(substring vr-reading-string (1+ idx))
	       ""))

;      (vr-log "**-- vr-output-filter: calling handler\n")
      (setq handler (cl-gethash vr-cmd vr-message-handler-hooks))
;      (vr-log (format "**-- vr-output-filter: handler=%S\n" handler))
      (if handler
	  (vr-execute-event-handler handler vr-request)

 	;; The VR process should fail gracefully if an expected
 	;; reply does not arrive...
 	(error "Unknown VR request: %s" vr-request))
      (vr-log "-- vr-output-filter: exiting")
    )
  )
)
     

(defun vr-send-reply (msg)
  (vr-log "-- vr-send-reply: msg=%S\n" msg)
  (if (and vr-dns-cmds (eq (process-status vr-dns-cmds) 'open))
      (progn
	(if (integerp msg)
	    (setq msg (int-to-string msg)))
	(if vr-log-send
	    (vr-log "<- r %s\n" msg))
;;; Alain what does that do? Should it be part of vr-serialize-message?
;;; 	(process-send-string vr-dns-cmds (vr-etonl (length msg)))

	(vr-log "**-- vr-send-reply: sending msg\n")
	(process-send-string vr-dns-cmds msg)
	(vr-log "**-- vr-send-reply: message sent... exiting.\n"))
    (message "VR Mode DNS reply channel is not open!"))
  )

(defun vr-send-cmd (msg)
  (vr-log (format "-- vr-send-cmd: msg=%S\n" msg))
  (if (and vr-emacs-cmds (eq (process-status vr-emacs-cmds) 'open))
      (progn
	(if vr-log-send
	    (vr-log "<- c %s\n" msg))
;;; Should this be part of vr-serialize-message???
;;;	(process-send-string vr-emacs-cmds (vr-etonl (length msg)))

	(vr-log (format "**-- vr-send-cmd: sending msg=%S\n" msg))
	(process-send-string vr-emacs-cmds msg))
    (message "VR Mode command channel is not open: %s" msg)))

;; ewww
(defun vr-etonl (i)
  (format "%c%c%c%c"
	  (lsh (logand i 4278190080) -24)
	  (lsh (logand i 16711680) -16)
	  (lsh (logand i 65280) -8)
	  (logand i 255)))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Subprocess commands
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defun vr-quit ()
  "Turn off VR mode, and cause the VR mode subprocess to exit cleanly."
  (interactive)
  (vr-mode 0))

(defun vr-toggle-mic ()
  "Toggles the state of the Dragon NaturallySpeaking microphone:
off -> on, {on,sleeping} -> off."
  (interactive)
  (vr-send-cmd "toggle-mic"))

(defun vr-show-window ()
  (interactive)
  (vr-send-cmd "show-window"))

(defun vr-hide-window ()
  (interactive)
  (vr-send-cmd "hide-window"))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Subprocess initialization, including voice commands.
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defun vr-connect (host port)
  (vr-log (format "**-- vr-connect: host=%S, port=%S\n" host port))
  (condition-case e
      (progn
	(vr-log "**-- vr-connect: opening vr-emacs-cmds\n")
 	(setq vr-emacs-cmds (open-network-stream "vr-emacs" nil
 						 host port))

	;;;
	;;; Connect an output filter to the Emacs commands network-stream
	;;; in case the speech server needs to to some handshaking on that
	;;; connection.
	;;;
	(set-process-filter vr-emacs-cmds 'vr-output-filter)
	(vr-log "**-- vr-connect: opened vr-emacs-cmds\n")
	(vr-log "connecting to speech server %s\n" vr-emacs-cmds)
	
	;;;
	;;; Possibly wait until Emacs has shaken hands with speech server
	;;; before opening second network stream.
	;;;
	(vr-log "**-- vr-connect: vr-wait-for-handshake-hook=%S\n" vr-wait-for-handshake-hook)
	(run-hooks 'vr-wait-for-handshake-hook)
	(vr-log "**-- vr-connect: AFTER vr-wait-for-handshake-hook\n")

	(setq vr-dns-cmds (open-network-stream "vr-dns" nil host (1+ port)))
	(vr-log "**-- vr-connect: connected to vr-dns-cmds\n")
	(process-kill-without-query vr-emacs-cmds)
	(process-kill-without-query vr-dns-cmds)
	(set-process-filter vr-dns-cmds 'vr-output-filter)
	(if vr-process
	    (set-process-filter vr-process nil))
	t)

    ('error (progn
	      (message "VR Mode: cannot connect to %s:%d" host port)
	      (message (format "Error condition was: %S" e))
	      (vr-mode 0)
	      nil)))
  (vr-log  "**-- vr-connect: exiting\n")

)

;; functionp isn't defined in Win 95 Emacs 19.34.6 (!??!?)
(defun vr-functionp (object)
  "Non-nil if OBJECT is a type of object that can be called as a function."
  (or (subrp object) (byte-code-function-p object)
      (eq (car-safe object) 'lambda)
      (and (symbolp object) (fboundp object))))

(defun vr-strip-dash (symbol)
  (concat (mapcar (lambda (x) (if (eq x ?-) ?\ x)) (symbol-name symbol))))


(defun vr-startup ()
  "Initialize any per-execution state of the VR Mode subprocess."

  (run-hooks 'vr-initialize-server-hook)

  ;; don't set up these hooks until after initialization has succeeded
  (add-hook 'post-command-hook 'vr-post-command)
  (add-hook 'minibuffer-setup-hook 'vr-enter-minibuffer)
  (vr-maybe-activate-buffer (current-buffer))
  (run-hooks 'vr-mode-startup-hook)
  )

(defun vr-kill-emacs ()
  (vr-mode 0)
  (sleep-for 1)
  t)

(defun vr-cmd-terminating (vr-request)
  (let (vr-emacs-cmds)
    (vr-mode 0))
  (if vr-host
      (vr-sentinel nil "finished\n"))
  (message "VR process terminated; VR Mode turned off")
  t)


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; VR Mode entry/exit
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defun vr-mode (arg &optional speech-server)
  "Toggle VR mode.  With argument ARG, turn VR mode on iff ARG is
positive.

The optional argument 'speech-server gives the name of the speech
server to configure VR Mode for (either 'vr or 'vcode). If not specified,
use whatever speech server VR Mode is currently configured for.

VR mode supports Dragon NaturallySpeaking dictation, Select 'N
Say(tm), and voice commands in Emacs buffers.  See README.txt for
instructions.

\\{vr-map}"
 (interactive "P")
  (vr-log "-- vr-mode: arg=%S\n" arg)

  (vr-log "**-- vr-mode: debug-on-error=%S\n" debug-on-error)
  (if speech-server
    (cond
      ((string= speech-server "vr") (vr-mode-configure-for-vr-server))
      ((string= speech-server "vcode") (vr-mode-configure-for-vcode-server))
    )
  )

  (vr-log "**-- vr-mode: after configuring for speech server\n")
  (vr-mode-activate arg)
  (vr-log "**-- vr-mode: after vr-mode-activate: exiting after configure-for-vr-server\n")
)

(defun vr-mode-activate (arg)
  "Activates the VR mode, after it has been configured for a particular
speech server"

  (vr-log "**-- vr-mode-activate: arg=%S, vr-mode=%S\n" arg vr-mode)
  (setq vr-mode
        (if (null arg) (not vr-mode)
 	  (> (prefix-numeric-value arg) 0)))
  (if vr-mode
      ;; Entering VR mode
      (progn
	(vr-log "starting VR mode %s\n" vr-host)
	(setq vr-reading-string nil)
	(setq vr-mic-state "not connected")
	(set-default 'vr-mode-line (concat " VR-" vr-mic-state))
	(setq vr-internal-activation-list vr-activation-list)
	(setq vr-cmd-executing nil)
	(add-hook 'kill-emacs-hook 'vr-kill-emacs)
	(run-hooks 'vr-mode-setup-hook)

	(if vr-host
	    (vr-connect vr-host vr-port)

;	  (setq vr-process (start-process "vr" vr-log-buff-name vr-command
;					  "-child"
;					  "-port" (int-to-string vr-port)))
	  (setq vr-process (start-process "vr" vr-log-buff-name "python" "E:\\VoiceCode\\VCode.TCP_IP\\Mediator\\tcp_server.py"))
	  (process-kill-without-query vr-process)
;	  (set-process-filter vr-process 'vr-output-filter)
	  (set-process-sentinel vr-process 'vr-sentinel))
	)
    
    ;; Leaving VR mode
    (remove-hook 'post-command-hook 'vr-post-command)
    (remove-hook 'minibuffer-setup-hook 'vr-enter-minibuffer)
    (remove-hook 'kill-buffer-hook 'vr-kill-buffer)
    (vr-activate-buffer nil)
    (if vr-host
	(vr-sentinel nil "finished\n")
      (vr-send-cmd "exit"))
    (run-hooks 'vr-mode-cleanup-hook)
    )
 (force-mode-line-update)
)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Configuration allowing vr-mode to interact with the VR.exe speech
;;; server.
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


(defun vr-mode-configure-for-vr-server ()
  "Configures VR Mode message for interacting with the VR.exe speech server."

  (vr-log "**-- vr-mode-configure-for-vr-server: called\n")

  (setq vr-sr-server-assumes-verbatim-dict t)
  (setq vr-dont-report-sr-own-changes t)

  ;;; Command for starting the speech server
  (setq vr-command "vr.exe")


  ;;; Function for waiting until Emacs has shaken hands with speech server
  ;;; For VR.exe server, we don't actually have to wait for handshake.
  (setq vr-wait-for-handshake-hook (lambda () nil))

  ;;; Functions for parsing/generating messages from/to speech server
  (setq vr-deserialize-message-hook 'vr-deserialize-message)
  (setq vr-serialize-message-hook 'vr-serialize-message)
  (setq vr-serialize-changes-hook 'vr-serialize-changes)

  ;;; Functions for sending messages to VR.exe
  (setq vr-send-kill-buffer-hook 'vr-send-kill-buffer)
  (setq vr-send-activate-buffer-hook 'vr-send-activate-buffer)
  (setq vr-send-deactivate-buffer-hook 'vr-send-deactivate-buffer)
  (add-hook 'kill-buffer-hook 'vr-kill-buffer)

  ;;; Function for handling errors in execution of commands received from 
  ;;; VR.exe.
  (setq vr-upon-cmd-error (lambda (req) nil))

  ;;; Functions for handling messages received from VR.exe
  (cl-clrhash vr-message-handler-hooks)
  (cl-puthash 'listening 'vr-cmd-listening vr-message-handler-hooks)
  (cl-puthash 'connected 'vr-cmd-connected vr-message-handler-hooks)
  (cl-puthash 'initialize 'vr-cmd-initialize vr-message-handler-hooks)
  (cl-puthash 'terminating 'vr-cmd-terminating vr-message-handler-hooks)
  (cl-puthash 'frame-activated 'vr-cmd-frame-activated vr-message-handler-hooks)

  ;;;
  ;;; Note: we have two hooks for 'heard-command. One for effecting the command
  ;;; and one for taking note of the command so it can later on be repeated
  ;;;
  (cl-puthash 'heard-command '(vr-cmd-heard-command vr-repeat-that-hook) vr-message-handler-hooks)
  (cl-puthash 'mic-state 'vr-cmd-mic-state vr-message-handler-hooks)
  (cl-puthash 'get-buffer-info 'vr-cmd-get-buffer-info vr-message-handler-hooks)
  (cl-puthash 'make-changes 'vr-cmd-make-changes vr-message-handler-hooks)
  (cl-puthash 'recognition 'vr-cmd-recognition vr-message-handler-hooks)
 
)

(defun vr-deserialize-message (message)
   "Parse a message serialized send by VR.exe as a sexp."

   (read-from-string message)
)

(defun vr-serialize-message (message)
  "Serialises a LISP data structure into a message that can be parsed by
   VR.exe" 

  (vr-log "-- vr-serialize-message: invoked\n")

  (let ((mess-name (car message)) (mess-content (cdr message)) (cmd))
    (cond

     ;;; Alain: Later on, put conditions for all the messages that VR.exe
     ;;; might need to receive.
     ((eq mess-name "change-text")
      (let ((beg (elt 0 )) ())
        (setq cmd (format "%s \"%s\" %d %d %d %d %s" 
 			 (elt mess-content 0) (elt mess-content 2) 
 			 (elt mess-content 3) (elt mess-content 4)
 			 (elt mess-content 5)))
      ))
     )
    (setq cmd (format "%s %s" mess-name cmd))
    (vr-log "-- vr-serialize-message: exited\n")
    cmd
  )
)


(defun vr-serialize-changes (change-list)
  "Creates a change notification message to be sent to VR.exe speech server.

Argument 'change-list is a list of 5ple:
   (repl-start repl-end repl-length buffer-tick repl-text)."

  (vr-log "-- vr-serialize-changes: invoked\n")
  (let ((mess "") (a-change) (repl-start) (repl-length) (repl-text))
    (if vr-changes-caused-by-sr-cmd
	;;;
	;;; If we are creating a change message that's a response to a 
	;;; request from the speech server, we must prefix the message 
	;;; with a buffer tick and the number of changes in the change
	;;; list.
	;;;
	(setq mess (format "%s%s%s" (buffer-modified-tick) 
			   (length change-list))))
	
    ;;;
    ;;; Now add a 'change-text message for each change in the change 
    ;;; list
    ;;;
    (while change-list
      (setq a-change (car change-list))
      (setq change-list (cdr change-list))
      (setq repl-start (nth 0 a-change))
      (setq repl-length (nth 1 a-change))
      (setq repl-text (nth 2 a-change))
      (setq mess (concat mess 
			 (format "change-text \"%s\" %d %d %d %d %s"
				 (buffer-name) (1- repl-start)
				 (+ (1- repl-start) repl-length) (repl-length)
				 (buffer-modified-tick)
				 (vr-string-replace repl-text "\n" "\\n"))))
      )
    (vr-log "-- vr-serialize-changes: exiting\n")
    mess
    )
)

(defun vr-initialize-server ()
  "Initialize the VR.exe speech server with a series of voice commands and 
grammars."
  (let ((l (lambda (x)
	     (cond ((eq x 'vr-default-voice-commands)
		    (mapcar l vr-default-voice-command-list))
		   ((symbolp x)
		    (vr-send-cmd
		     (concat "define-command "
			     (vr-strip-dash x) "|" (symbol-name x))))
		   ((and (listp x) (eq (car x) 'list))
		    (vr-send-cmd
		     (format "define-list %s|%s" (nth 1 x) (nth 2 x))))
		   ((and (consp x) (vectorp (cdr x)))
		    (vr-send-cmd
		     (format "define-command %s|%s" (car x) (cdr x))))
		   ((and (consp x) (symbolp (cdr x)))
		    (vr-send-cmd
		     (format "define-command %s|%s" (car x) (cdr x))))
		   ((and (consp x) (stringp (cdr x)))
		    (vr-send-cmd
		     (format "define-command %s|%s" (car x) (cdr x))))
		   (t
		    (error "Unknown vr-voice-command-list element %s"
			   x))
		   )
	     )))
    (mapcar l (if (eq vr-voice-command-list t)
		  vr-default-voice-command-list
		vr-voice-command-list)))
)

(defun vr-send-kill-buffer ()
   "Sends a 'kill-buffer message to VR.exe"
   (let ()
     (vr-log "-- vr-send-kill-buffer: invoked\n")
     (vr-send-cmd  (concat "kill-buffer " (buffer-name (current-buffer))))
     (vr-log "-- vr-send-kill-buffer: exited\n")
   )
)


(defun vr-send-activate-buffer ()
   "Sends a 'activate-buffer message to VR.exe"
   (let ()
     (vr-send-cmd  (concat "activate-buffer " (buffer-name (vr-buffer))))
   )
)

(defun vr-send-deactivate-buffer ()
   "Sends a 'deactivate-buffer message to VR.exe"
   (let ()
     (vr-send-cmd  (concat "deactivate-buffer " (buffer-name (vr-buffer))))
   )
)


(defun vr-cmd-listening (vr-request)
  (vr-connect "127.0.0.1" (nth 1 vr-request))
  t)
(defun vr-cmd-connected (vr-request)
  (vr-send-cmd (run-hook-with-args 'vr-serialize-message-hook 
		     (list "initialize"
		      (list 
		       (if (equal vr-win-class "")
			   nil
			 vr-win-class)
		       (if (equal vr-win-title "")
			   nil
			 vr-win-title)
		       (cdr (assoc 'window-id
				   (frame-parameters (car
						      (visible-frame-list)))))))))
  t)


(defun vr-cmd-initialize (vr-request)
  "Function that is called when the VR Mode command \"initialize\" is
received. The function receives a single argument, REQ,
which is the list representing the command and its arguments."
  (cond ((eq (nth 1 vr-request) 'succeeded)
	 (vr-startup))
	((eq (nth 1 vr-request) 'no-window)
	 (vr-mode 0)
	 (message "VR process: no window matching %s %s"
		  vr-win-class vr-win-title))
	(t
	 (vr-mode 0)
	 (message "VR process initialization: %s"
		  (nth 1 vr-request))))
  t)


(defun vr-cmd-frame-activated (vr-request)

  (vr-log "-- vr-cmd-frame-activated: invoked\n")

  ;; This is ridiculous, but Emacs does not automatically change its
  ;; concept of "selected frame" until you type into it.  So, we have
  ;; the subprocess send us the HWND value and explcitly activate the
  ;; frame that owns it.  The HWND may not belong to any frame, for
  ;; example if vr-win-class/title match a Windows window not
  ;; belonging to Emacs.  In that case, just ignore it.
  ;;
  (let* ((wnd (int-to-string (car (cdr vr-request))))
	 (frame (car (vr-filter
		      (lambda (f) (equal (cdr (assoc 'window-id
						     (frame-parameters f)))
					 wnd))
		      (visible-frame-list)))))
    (if frame
	(select-frame frame)
      (message "VR Mode: %s is not an Emacs frame window handle; ignored."
	       wnd)))
  (vr-maybe-activate-buffer (current-buffer))

  (vr-log "-- vr-cmd-frame-activated: exiting\n")

  t)

(defun vr-cmd-heard-command (vr-request)
  ;;
  ;; We want to execute the command after this filter function
  ;; terminates, so add the key sequence to invoke it to the end of
  ;; unread-command-events.  Add the key binding, if any, so we don't
  ;; get the "you can run the command <cmd> by typing ..." message.
  ;;
  ;; If the command has arguments, invoke it directly instead.  Also,
  ;; invoke pre-command-hook and post-command-hook so it looks as much
  ;; like a regular command as possible.
  ;;
  ;; Set vr-cmd-executing so vr-post-command (hook) will inform VR.EXE
  ;; when the command is finished.  If cmd is an undefined key
  ;; sequence, no command will be executed, so complete immediately.
  ;;
  (let* ((cmd (nth 1 vr-request))
	 (kseq (or (and (vectorp cmd) cmd)
		   (where-is-internal cmd nil 'non-ascii)
		   (concat "\M-x" (symbol-name cmd) "\n"))))
    (setq vr-cmd-executing (if (vectorp cmd) (key-binding cmd) cmd))
    (if (not vr-cmd-executing)
	(vr-send-cmd "command-done undefined"))
    
    (if (not (vectorp cmd))
	(vr-execute-command (cdr vr-request))
      (vr-log "running %s as key sequence:\n" cmd )
      (setq unread-command-events
	    (append unread-command-events
		    (listify-key-sequence kseq)))
      ) 
	)
  t)


(defun vr-cmd-mic-state (vr-request)
  (let ((state (car (cdr vr-request))))
    (cond ((eq state 'off)
	   (setq vr-mic-state "off"))
	  ((eq state 'on)
	   (setq vr-mic-state "on"))
	  ((eq state 'sleep)
	   (setq vr-mic-state "sleep")))
    (vr-activate-buffer vr-buffer))
  t)


(defun vr-cmd-get-buffer-info (vr-request)
  (let ((buffer (nth 1 vr-request))
	(tick (nth 2 vr-request))
	vr-text)
    (vr-log "get-buffer-info: current buffer: %s vr-buffer:%s\n"
	    (buffer-name) vr-buffer)
    (if (not (equal vr-buffer (get-buffer buffer)))
	(progn
	  (ding)
	  (message "VR Mode: get-buffer-info: %s is not %s"
		   buffer (buffer-name vr-buffer))    

	  ;; make sure that we always give information for the buffer that
	  ;; was asked for, even if we ding and the wrong buffer is
	  ;; selected.  This almost certainly means that the subprocess
	  ;; has not had time to update its idea of current buffer
	  (save-excursion
	    (set-buffer (get-buffer buffer))
	    (vr-log "buffer synchronization problem: using %s\n" 
		    (buffer-name (current-buffer)))
	    (vr-send-reply (1- (point)))
	    (vr-send-reply (1- (point)))
	    (vr-send-reply (1- (window-start)))
	    (vr-send-reply (1- (window-end)))
	    (if (eq (buffer-modified-tick) tick)
		(vr-send-reply "0 not modified")
	      (vr-send-reply "1 modified")
	      (vr-send-reply (format "%d" (buffer-modified-tick)))
	      (setq vr-text (buffer-string))
	      (vr-send-reply (length vr-text))
	      (vr-send-reply vr-text))
	    ))

      ;;
      ;; If mouse-drag-overlay exists in our buffer, it
      ;; overrides vr-select-overlay.
      ;;
      (let* ((mdo mouse-drag-overlay)
	     (sel-buffer (overlay-buffer mdo)))
	(vr-log " %s %s \n" vr-select-overlay sel-buffer)
	(if (eq sel-buffer vr-buffer)
	    (move-overlay vr-select-overlay
			  (overlay-start mdo)
			  (overlay-end mdo)
			  sel-buffer)))

      ;;
      ;; Send selection (or point) and viewable window.
      ;;
      (let ((sel-buffer (overlay-buffer vr-select-overlay)))
	(if (eq sel-buffer vr-buffer)
	    (progn
	      (vr-send-reply (1- (overlay-start vr-select-overlay)))
	      (vr-send-reply (1- (overlay-end vr-select-overlay)))
	      )
	  (vr-send-reply (1- (point)))
	  (vr-send-reply (1- (point)))
	  ))
      (vr-send-reply (1- (window-start)))
      (vr-send-reply (1- (window-end)))
      ;;
      ;; Then, send buffer contents, if modified.
      ;;

      (if (and (not vr-resynchronize-buffer) (eq (buffer-modified-tick) tick))
	  (vr-send-reply "0 not modified")
	(if vr-resynchronize-buffer
	    (vr-log "buffer resynchronization requested \n"))
	(vr-send-reply "1 modified")
	(vr-send-reply (format "%d" (buffer-modified-tick)))
	(setq vr-text (buffer-string))
	(vr-send-reply (length vr-text))
	(vr-send-reply vr-text)
	(setq vr-resynchronize-buffer nil))))
  t)

(defun 	vr-func-is-bound-to-a-key (func)
  ;;;
  ;;; For now, just handle self-insert characters and \n
  ;;; It might make more sense in the future to lookup all the key
  ;;; bindings and look for an occurence of func
  ;;;
  (vr-log "-- vr-func-is-bound-to-a-key: func=%S\n" func)
  (vr-log "--** vr-func-is-bound-to-a-key: (type-of func)=%S\n" (type-of func))
  (or 
   (equal func 'self-insert-command)
   (vr-log "--** vr-func-is-bound-to-a-key: after equals func 'self-insert\n")
   (equal func (key-binding "\n"))
   (vr-log "--** vr-func-is-bound-to-a-key: exiting\n"))
)

(defun vr-exec-change-and-report-responses (repl-start repl-length repl-text)

  "Effects a change to the current buffer, and reports what Emacs did
in response to it."


  ;;; 
  ;;; First delete the region to change
  ;;;
  (let ((vr-ignore-changes 
	 (if vr-dont-report-sr-own-changes 'delete)))
    (delete-region repl-start (+ repl-start repl-length))
    )

  (vr-log "--** vr-exec-change-and-report-responses: after delete-region\n")


  ;;;
  ;;; Now insert the new text
  ;;;
  (goto-char repl-start)
  (let ((vr-ignore-changes 
	 (if vr-dont-report-sr-own-changes 'self-insert)))

    (vr-log "--** vr-exec-change-and-report-responses: starting to send keystrokes\n")

    ;;we make the changes by inserting the appropriate
    ;;keystrokes and evaluating them
    (setq unread-command-events
	  (append unread-command-events
		  (listify-key-sequence repl-text)))

    (vr-log "--** vr-exec-change-and-report-responses: after listify key-sequence\n")

    (while unread-command-events
      (let* ((event(read-key-sequence-vector nil))
	     (command (key-binding event))
	     (this-command command)
	     (last-command-char (elt event 0))
	     (last-command-event (elt event 0))
	     (last-command-keys event)
	     )
	(vr-log "key-sequence %s %s %s\n" event
		command last-command-char)
	(run-hooks 'pre-command-hook)
	(if (vr-func-is-bound-to-a-key command)
	    (progn
	      (command-execute command nil)
	      (vr-log "--** vr-exec-change-and-report-responses: after executing command=%S, (point)=%S" command (point))
	      )
	  (vr-log "command is not a bound to a key: %s\n"
		  command )
	  ;; send back a "delete command", since when
	  ;; command is executed it will send the insertion.
	  (if vr-sr-server-assumes-verbatim-dict
	      (let ((cmd (list 
			  (1- (point))  1 ""))
		    (vr-ignore-changes 
		     (if vr-dont-report-sr-own-changes 
			 'command-insert)))
		(setq vr-queued-changes (cons cmd
					      vr-queued-changes))
		;; exit-minibuffer is a command that does not
		;; return properly , so to avoid timeouts waiting
		;; for the replies, we put it in the deferred
		;; function
		(if (memq command vr-nonlocal-exit-commands )
		    (setq vr-deferred-deferred-function command )
		  (command-execute command nil))
		(vr-log "executed command: %s\n" command)
		)))
	(run-hooks 'post-command-hook)
	)))		      
)

(defun vr-cmd-make-changes (vr-request)
   (vr-log "-- vr-cmd-make-changes: invoked, vr-request=%S\n" vr-request)

   (if (eq (current-buffer) vr-buffer)
      
      (let ((start (nth 0 vr-request))
 	    (num-chars (nth 1 vr-request))
 	    (text (nth 2 vr-request))
 	    (sel-start (nth 3 vr-request))
 	    (sel-chars (nth 4 vr-request))
 	    (indent-start (nth 5 vr-request))
 	    (indent-length (nth 6 vr-request))
	    (region-should-be-unindented (nth 7 vr-request))
	    (n-indent-levels (nth 8 vr-request))
 	    vr-queued-changes)

        ;;; deb
	(if (string= "\n" text) (vr-log "--** vr-cmd-make-changes: inserting \\n!\n"))
        ;;; fin


	(vr-log "--** vr-cmd-make-changes: vr-buffer is current\n")
	(vr-log "--** vr-cmd-make-changes: start=%s, num-chars=%S, text='%S', sel-start=%S, sel-chars=%S, indent-start=%S, indent-length=%S\n" start num-chars text sel-start sel-chars indent-start indent-length)

 	(if (and buffer-read-only (or (< 0 num-chars) (< 0 (length text)))
 		 vr-sr-server-assumes-verbatim-dict)
 	    ;; if the buffer is read-only we don't make any changes
 	    ;; to the buffer, and instead we send the 
 	    ;; the inverse command back. This is in effect, tells the 
 	    ;; speech server that the text it thought got inserted as
 	    ;; a result of the utterance, immediatly got deleted.
 	    (progn
 	      (vr-log "make changes:Buffer is read-only %d %d\n"
 		      num-chars (length text))
 	      (if vr-sr-server-assumes-verbatim-dict
 		  (let ((cmd (list 
			      (1- start) 
			      (length text) 
			      (buffer-substring start
						(+ start num-chars)))))
 		    (setq vr-queued-changes (cons cmd
 						  vr-queued-changes)))
		)
	      )
 		
	  (vr-log "--** vr-cmd-make-changes: current buffer is not read only\n")

	  ;; if buffer is not read-only we perform the changes as before
	  (vr-exec-change-and-report-responses start num-chars text)

	  (vr-log "--** vr-cmd-make-changes: done sending keystrokes\n")

	  ;; whether or not we should put point where
	  ;; NaturallySpeaking wants is not so easy to decide.  If
	  ;; point is not there, dictation won't work correctly if
	  ;; there are characters in front of point.  On the other
	  ;; hand, keys can be bound to multiple characters, and
	  ;; deferred functions can move point in which case
	  ;; NaturallySpeaking has no idea where it should be.  This
	  ;; is some kind of heuristic.
	  (if (equal (length text) 0)
	      ;; this is a pure selection or cursor repositioning,
	      ;; just put it there
	      (progn
		(vr-log "make changes: putting point at %s\n" sel-start)
		(goto-char sel-start))
	    ;; Text is being inserted, so we move point to where it
	    ;; should be relative to the end of the string we got from
	    ;; NaturallySpeaking.  This should work even if keys are
	    ;; bound to multiple characters, and surprisingly enough
	    ;; even if deferred functions have moved point completely!
	    (vr-log "make changes: positioning point relative\n")
	    (goto-char (+ (point)
			  (- sel-start (+ start (length text)))))
	    )

	  (vr-log "--** vr-cmd-make-changes: done with (if (equal (length text) 0)\n")

	  ;;;
	  ;;; Indent/Unindent the requested region.
	  ;;; This will keep the cursor at the "logical" place where it 
	  ;;; was before indentation. In other words, it won't stay at the
	  ;;; exact char-offset where it was, but will move along with the
	  ;;; automatic indentation.
	  ;;;
	  (if region-should-be-unindented
	      (vcode-unindent-region (indent-start 
				      (+ indent-start indent-length) 
				      n-indent-levels)
	    (indent-region indent-start (+ indent-start indent-length) nil))


	  (delete-overlay mouse-drag-overlay)
	  (if (equal sel-chars 0)
	      (delete-overlay vr-select-overlay)
	    (move-overlay vr-select-overlay
			  sel-start (+ sel-start sel-chars)
			  (current-buffer))))

	(vr-log "--** vr-cmd-make-changes: sending queued changes\n")

 	;; in any case, we send the replies and the queued changes.
	(if vr-changes-caused-by-sr-cmd
	    (vr-send-reply
	      (setq message 
		    (run-hook-with-args 
		     'vr-serialize-changes-hook
		     (nreverse vr-queued-changes))))
	  )

	(vr-log "--** vr-cmd-make-changes: DONE sending queued changes)")

	(if vr-deferred-deferred-function
	    (progn
	      (vr-log "executing deferred function in make-changes: %s\n"
		      vr-deferred-deferred-function)
	      (setq vr-deferred-deferred-deferred-function
		    vr-deferred-deferred-function )
	      (setq vr-deferred-deferred-function nil)
	      (fix-else-abbrev-expansion)
	      (vr-execute-command vr-deferred-deferred-deferred-function)))
 	)
    ;; if the current buffer is not VR-buffer
    (vr-send-reply "-1")))

   (vr-log "-- vr-cmd-make-changes: exited")

t)

;; This function is called by Dragon when it begins/ends mulling over an
;; utterance; delay key and mouse events until it is done.  This
;; ensures that key and mouse events are not handled out of order
;; with respect to speech recognition events
(defun vr-cmd-recognition (vr-request)
  (let ((state (nth 1 vr-request)))
    (progn
      (vr-log (format "-- vr-cmd-recognition: vr-request=%S\n" vr-request))
      (vr-log "recognition %s: current buffer: %s vr-buffer:%s\n"
	      state (buffer-name) vr-buffer)
      (cond ((eq state 'begin)
					; if recognition starts and VR
					; buffer is not the current
					; buffer, we might have a
					; potential problem with
					; synchronization.  In that
					; case, let's try calling
					; maybe-activate-buffer and
					; see if it's not already too
					; late.
	     (vr-maybe-activate-buffer (current-buffer))
	     (run-at-time 0 nil 'vr-sleep-while-recognizing)
	     (setq vr-recognizing t))
	    ((eq state 'end)
	     (setq vr-recognizing nil))
	    (t
	     (error "Unknown recognition state: %s" state)))))

  (vr-log "-- vr-cmd-recognition: exiting\n")

  t)


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; "Repeat that N times"
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defvar vr-last-heard-command-request nil
  "If non-nil, the complete, most-recently-received heard-command
message from VR.EXE")

(defun vr-repeat-that-hook (vr-request)
  (let ((cmd (nth 1 vr-request)))
    (if (not (eq cmd 'vr-repeat-that))
	(setq vr-last-heard-command-request vr-request)))
  nil)

(defun vr-repeat-that (num)
  (interactive '(1))
  (if vr-last-heard-command-request
      (progn
	(while (> num 0)
	  (run-hook-with-args-until-success 'vr-cmd-heard-command-hook
					    vr-last-heard-command-request)
	  (setq num (1- num))))))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Repeating commands (based on code by Steve Freund).
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defvar vr-repeat-rate nil
  "The rate at which to repeat commands, in seconds.  If nil, any
currently repeating command will terminate.")

(defun vr-repeat-cmd (freq cmd &rest args)
  "Every FREQ seconds, execute (CMD ARG ...), until the user
generates an input event such as a key press or mouse click (or
executes a voice command that does so).

If the event is RET (the return key), it terminates the repeat but is
then discarded.  Any other event terminates the repeat and is then
acted on as it normally would be."
  (let (ev)
    (discard-input)
    (setq vr-repeat-rate freq)
    (while vr-repeat-rate
      (apply cmd args)
      (sit-for vr-repeat-rate)
      (if (input-pending-p)
	  (progn
	    (setq ev (read-event))
	    (setq vr-repeat-rate nil))))
    (if (and ev (not (eq ev 'return)))
	(setq unread-command-events
	      (cons ev unread-command-events)))
    ))

(defun vr-repeat-mult-rate (f)
  "Multiply the number of seconds between each execution of the current
repeating command by FACTOR."
  (setq vr-repeat-rate (* vr-repeat-rate f)))

(defun vr-repeat-stop (d)
  "Terminate the current repeating command."
  (setq vr-repeat-rate nil))

(defmacro vr-make-repeat-cmd (name freq cmd &rest args)
  "Define an interactive repeating command called NAME that takes no
arguments and, every FREQ seconds, invokes the function CMD.  Uses
vr-repeat-cmd."
  (let ((vrc 'vr-repeat-cmd))
    (list 'defun name '()
	  (format "Invoke %s every %s seconds,\nusing vr-repeat-cmd (which see)."
		  cmd freq)
	  '(interactive)
	  (list 'apply (list 'quote vrc) freq (list 'quote cmd)
		(list 'quote args)))))

(vr-make-repeat-cmd vr-repeat-move-up-s 0.25 previous-line 1)
(vr-make-repeat-cmd vr-repeat-move-up-f 0.05 previous-line 1)
(vr-make-repeat-cmd vr-repeat-move-down-s 0.25 next-line 1)
(vr-make-repeat-cmd vr-repeat-move-down-f 0.05 next-line 1)

(vr-make-repeat-cmd vr-repeat-move-left-s 0.25 backward-char 1)
(vr-make-repeat-cmd vr-repeat-move-left-f 0.05 backward-char 1)
(vr-make-repeat-cmd vr-repeat-move-right-s 0.25 forward-char 1)
(vr-make-repeat-cmd vr-repeat-move-right-f 0.05 forward-char 1)

(vr-make-repeat-cmd vr-repeat-move-word-left-s 0.25 backward-word 1)
(vr-make-repeat-cmd vr-repeat-move-word-left-f 0.05 backward-word 1)
(vr-make-repeat-cmd vr-repeat-move-word-right-s 0.5 forward-word 1)
(vr-make-repeat-cmd vr-repeat-move-word-right-f 0.05 forward-word 1)

(vr-make-repeat-cmd vr-repeat-search-forward-s 0.75 isearch-repeat-forward)
(vr-make-repeat-cmd vr-repeat-search-forward-f 0.25 isearch-repeat-forward)
(vr-make-repeat-cmd vr-repeat-search-backward-s 0.75 isearch-repeat-backward)
(vr-make-repeat-cmd vr-repeat-search-backward-f 0.25 isearch-repeat-backward)

(defun vr-repeat-kill-line (freq)
  "Invoke kill-line every FREQ seconds, using vr-repeat-cmd (which see).
The lines killed with this command form a single block in the yank buffer."
  (kill-new "") 
  (vr-repeat-cmd freq (function (lambda () (kill-line) (append-next-kill)))))

(defun vr-repeat-yank (freq arg)
  "Perform a yank from the kill ring every FREQ seconds, using
vr-repeat-cmd (which see).  This function cycles through the yank
buffer, doing the right thing regardless of whether the previous
command was a yank or not."
  (interactive (list 0.5 (prefix-numeric-value prefix-arg)))
  (vr-repeat-cmd
   freq (function (lambda ()
		    (if (or (eq last-command 'yank) (eq this-command 'yank))
			(yank-pop arg)
		      (yank arg)
		      (setq last-command 'yank))
		    (undo-boundary)
		    ))))


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Configuration allowing vr-mode to interact with VoiceCode speech 
;;; server.
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(setq load-path (append load-path (list (substitute-in-file-name "$VCODE_HOME/Environments/Emacs"))))
(load "messaging")

(defvar vcode-app-id nil 
"Unique ID assigned to this instance of Emacs by the VoiceCode server.")

(defun vcode-make-all-keys-self-insert ()
  
)

(defun vr-mode-configure-for-vcode-server ()
  "Configures VR Mode for interacting with the VoiceCode speech server."

  (vr-log "**-- vr-mode-configure-for-vcode-server: called\n")

  ;;;
  ;;; VCode will do automatic indentation and stuff.
  ;;;
  (vcode-make-all-keys-self-insert)

  (setq vr-sr-server-assumes-verbatim-dict nil)
  (setq vr-dont-report-sr-own-changes nil)

  ;;;
  ;;; Hook function that waits for Emacs to handshake with first 
  ;;; socket connection before connecting a second time.
  ;;;
  (setq vcode-app-id nil)
  (setq vr-wait-for-handshake-hook 'vcode-wait-for-handshake)

  ;;;
  ;;; Hook functions for parsing/generating messages to/from VCode server
  ;;;
  (setq vr-deserialize-message-hook 'vcode-deserialize-message)
  (setq vr-serialize-message-hook 'vcode-serialize-message)
  (setq vr-serialize-changes-hook 'vcode-serialize-changes)

  ;;;
  ;;; Hook function for starting the VCode server
  ;;;
  (setq vr-command (substitute-in-file-name "%VCODE_HOME%/Mediator/vcode.bat"))
  
  ;;; Functions for sending messages to VR.exe
  (setq vr-send-kill-buffer-hook 'vcode-send-kill-buffer)
  (setq vr-send-activate-buffer-hook 'vcode-send-activate-buffer)
  (setq vr-send-deactivate-buffer-hook 'vcode-send-deactivate-buffer)
  (add-hook 'kill-buffer-hook 'vr-kill-buffer)

  ;;; Function for handling errors in execution of commands received from 
  ;;; VR.exe.
  (setq vr-upon-cmd-error 'vcode-send-cmd-error-message)


  ;;;
  ;;; Hook functions for handling messages received from VCode
  ;;; 
  (cl-clrhash vr-message-handler-hooks)

  ;;;
  ;;; These messages are sent by VCode during handshake part of the 
  ;;; protocol
  ;;;
  (cl-puthash 'send_app_name 'vcode-cmd-send-app-name vr-message-handler-hooks)
  (cl-puthash 'your_id_is 'vcode-cmd-your-id-is vr-message-handler-hooks)
  (cl-puthash 'send_id 'vcode-cmd-send-app-id vr-message-handler-hooks)
  (cl-puthash 'terminating 'vr-cmd-terminating vr-message-handler-hooks)


  (cl-puthash 'recog_begin 'vcode-cmd-recognition-start 
	      vr-message-handler-hooks)
  (cl-puthash 'recog_end 'vcode-cmd-recognition-end 
	      vr-message-handler-hooks)
  (cl-puthash 'active_buffer_name 'vcode-cmd-active-buffer-name 
	      vr-message-handler-hooks)
  (cl-puthash 'open_file 'vcode-cmd-open-file vr-message-handler-hooks)
  (cl-puthash 'confirm_buffer_exists 'vcode-cmd-confirm-buffer-exists vr-message-handler-hooks)
  (cl-puthash 'list_open_buffers 'vcode-cmd-list-open-buffers vr-message-handler-hooks)
  (cl-puthash 'close_buffer 'vcode-cmd-close-buffer vr-message-handler-hooks)
  (cl-puthash 'file_name 'vcode-cmd-file-name vr-message-handler-hooks)
  (cl-puthash 'language_name 'vcode-cmd-language-name vr-message-handler-hooks)
  (cl-puthash 'line_num_of 'vcode-cmd-line-num-of vr-message-handler-hooks)
  (cl-puthash 'cur_pos 'vcode-cmd-cur-pos vr-message-handler-hooks)
  (cl-puthash 'get_selection 'vcode-cmd-get-selection vr-message-handler-hooks)
  (cl-puthash 'get_text 'vcode-cmd-get-text vr-message-handler-hooks)
  (cl-puthash 'get_visible 'vcode-cmd-get-visible vr-message-handler-hooks)
  (cl-puthash 'len 'vcode-cmd-len vr-message-handler-hooks)
  (cl-puthash 'newline_conventions 'vcode-cmd-newline-conventions vr-message-handler-hooks)
  (cl-puthash 'pef_newline_convention 'vcode-cmd-pref-newline-conventions vr-message-handler-hooks)

  ;;;
  ;;; These messages are used by VCode to change the content of the buffer
  ;;;
  (cl-puthash 'set_selection 'vcode-cmd-set-selection vr-message-handler-hooks)
;;; Is this needed?
;;;  (cl-puthash 'make_position_visible 'vcode-cmd-make-position-visible vr-message-handler-hooks)
  (cl-puthash 'move_relative_page 'vcode-cmd-move-relative-page vr-message-handler-hooks)  
  (cl-puthash 'insert 'vcode-cmd-insert vr-message-handler-hooks)  
;;;  (cl-puthash 'insert_indent 'vcode-cmd-insert-indent vr-message-handler-hooks)  
  (cl-puthash 'indent 'vcode-cmd-indent vr-message-handler-hooks)  
  (cl-puthash 'delete 'vcode-cmd-delete vr-message-handler-hooks)  
  (cl-puthash 'goto 'vcode-cmd-goto vr-message-handler-hooks)  

  ;;;
  ;;; These ones are currently not handled by VCode, but they probably should
  ;;;
;  (cl-puthash 'heard-command 'vr-cmd-heard-command-hook vr-message-handler-hooks)
;  (cl-puthash 'mic-state 'vr-cmd-mic-state-hook vr-message-handler-hooks)



  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ;;; These messages are defined in VR.exe but don't seem useful for VCode.
  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;  (cl-puthash 'listening 'vr-cmd-listening-hook vr-message-handler-hooks)

;;; In VR.exe, this message is sent only to confirm
;;; that there is indeed a window with the ID, title or class that Emacs
;;; sent upon connection. But VCode doesn't expect Emacs to tell it about
;;; its window (it decides that for itself by looking at what is the active
;;; window)
;  (cl-puthash 'connected 'vcode-cmd-connected-hook vr-message-handler-hooks)

;;; See comment about 'vcode-cmd-connected-hook
;  (cl-puthash 'initialize 'vr-cmd-initialize-hook vr-message-handler-hooks)

;;; VCode will tell Emacs that a frame is activated when
;;; it sends a recog_begin message
;  (cl-puthash 'frame-activated 'vr-cmd-frame-activated-hook vr-message-handler-hooks)

;;; Not needed in VCode. VCode will send separate requests for different
;;; parts of the buffer info separately.
;  (cl-puthash 'get-buffer-info 'vr-cmd-get-buffer-info vr-message-handler-hooks)

;;; Not needed in VCode. VCode will send different messages to make different
;;; kinds of changes.
;  (cl-puthash 'make-changes 'vr-cmd-make-changes vr-message-handler-hooks)


  (vr-log "**-- vr-mode-configure-for-vcode-server: exited\n")
)


(defun vcode-serialize-message (mess)
  "Serializes a LISP data structure into a string message that can be sent to 
VoiceCode server."
;  (vr-log (format "-- vcode-serialize-message: mess=%S\n" mess))
  (let ((mess-name (elt mess 0)) (mess-cont (elt mess 1)))
    (vr-log (format "**-- vcode-serialize-message: mess-name=%S\n" mess-name))
    (setq serialized-mess (vcode-pack-mess (vcode-encode-mess mess-name mess-cont)))
;    (vr-log "-- vcode-serialize-message: exiting\n")
    serialized-mess
  )
)

(defun vcode-deserialize-message (mess)
  "Deserializes a string message received from the VoiceCode server 
into a LISP data structure."

  (vr-log (format "**-- vcode-deserialize-message: (length mess)=%S, mess=%S\n" (length mess) mess))
  (let ((unpack-result) (unpacked-mess) (bytes-parsed) 
	(mess-name) (mess-cont))

    ;;;
    ;;; Unpack the message
    ;;;
    (setq unpack-result (vcode-unpack-mess mess))
    (setq unpacked-mess (elt unpack-result 0))
;    (vr-log (format "**-- vcode-deserialize-message: unpacked-mess=%S\n" unpacked-mess))
    (setq bytes-parsed (elt unpack-result 1))
;    (vr-log (format "**-- vcode-deserialize-message: bytes-parsed=%S\n" bytes-parsed))

    ;;;
    ;;; Then decode it
    ;;; 
;    (vr-log "**-- vcode-deserialize-message: before vcode-decode-mess\n")
    (setq mess (vcode-decode-mess unpacked-mess ))
;    (vr-log "**-- vcode-deserialize-message: after vcode-decode-mess, mess=%S\n" mess)
    (setq mess-name (elt mess 0))
;    (vr-log "**-- vcode-deserialize-message: after setq mess-name\n")
    (setq mess-cont (elt mess 1))
;    (vr-log "**-- vcode-deserialize-message: after setq mess-cont\n")
    (vr-log "**-- vcode-deserialize-message: exiting with mess-name=%S, mess-cont=%S\n, bytes-parsed=%S\n" mess-name mess-cont bytes-parsed)
    (list (list mess-name mess-cont) bytes-parsed)
  )
)

(defun vcode-send-cmd-error-message (vcode-req)

  "Sends error message an error message to VCode. The error was
generated while executing VCode request 'vcode-req."

;   (let ((mess-name (concat (elt 0 vcode-req) "_resp"))
;        (mess-cont make-hash-table :test 'string=))
;     (cl-sethash "error" 1 mess-cont)
;     (vr-send-reply 
;      (run-hook-with-args 
;       'vr-serialize-message-hook (list mess-name mess-cont)))
;     )

)

(defun vcode-cmd-send-app-name (vcode-req)
   "Sends the name of the application ('Emacs) to the VoiceCode server."

   (vr-log (format "**-- vcode-cmd-send-app-name: vcode-req=%S\n" vcode-req))

   (let ((mess-cont (make-hash-table :test 'string=)))
     (cl-puthash "value" "emacs" mess-cont)
     (vr-send-cmd (run-hook-with-args 'vr-serialize-message-hook (list "app_name" mess-cont)))
  )

   (vr-log "**-- vcode-cmd-send-app-name: exiting\n")
)

(defun vcode-cmd-your-id-is (vcode-req)
   "Stores the unique ID assigned by VoiceCode to this instance of Emacs, so 
we can send it back to VoiceCode when we ask it for a second network connection."

   (vr-log (format "**-- vcode-cmd-your-id-is: vcode-req=%S\n" vcode-req))
   (let ((mess-name (elt vcode-req 0)) (mess-cont (elt vcode-req 1))
	 (ok-mess-cont (make-hash-table :key 'string=)))
     (vr-log (format "-- vcode-cmd-your-id-is: vcode-req=%S\n" vcode-req))


     (vr-log (format "**-- vcode-cmd-your-id-is: sending \"ok\", (hash-items ok-mess-cont)=%S\n" (hash-items ok-mess-cont)))
     (vr-send-cmd (run-hook-with-args 'vr-serialize-message-hook (list "ok" ok-mess-cont)))

     ;;;
     ;;; Wait til the very end before setting 'vcode-app-id, because that will
     ;;; cause 'vcode-wait-for-handshake to exit, which will in turn
     ;;; start the second network connection (and we don't want the second
     ;;; connection to start before VCode server has received the 'ok message
     ;;; and reacted to it).
     ;;;
     (setq vcode-app-id (cl-gethash "value" mess-cont))
   )
   (vr-log (format "**-- vcode-cmd-your-id-is: exiting, vcode-app-id=%S" vcode-app-id))
)

(defun vcode-cmd-send-app-id (vcode-req)

   "Sends the unique ID received from VCode server (when opened first
network connection to it) back to the VCode server.

This allows the VCode server to know for sure that the second network
connection originates from the same Emacs instance as the first one."

   (vr-log (format "-- vcode-cmd-send-app-id: vcode-req=%S, vcode-app-id=%S\n" vcode-req vcode-app-id))

   (let ((mess-cont (make-hash-table :test 'string=)))

     ;;; Then send that ID back to the server
     (cl-puthash "value" vcode-app-id mess-cont)
     (vr-log (format "**-- vcode-cmd-send-app-id: sending \"my_id_is\", (hash-items mess-cont)=%S\n" (hash-items mess-cont)))
     (vr-send-reply (run-hook-with-args 'vr-serialize-message-hook (list "my_id_is" mess-cont)))


     ;;;
     ;;; Invoke 'vr-startup explicitly here because VCode server never sends an
     ;;; 'inialize message.
     ;;;
     (vr-startup)

     (vr-log "**-- vcode-cmd-send-app-id: DONE sending \"my_id_is\"")
   )
)

(defun vcode-wait-for-handshake ()
  "This function waits until Emacs has shaken hands with VoiceCode server
on the first socket connection. We know the handshake has happened when
Emacs has set 'vcode-app-id to a non nil value."

  (vr-log "**-- vcode-wait-for-handshake: called, vcode-app-id=%S\n" vcode-app-id)

;  (sleep-for 30)
  (while (not vcode-app-id)
    (progn
      (vr-log "**-- vcode-wait-for-handshake: still waiting, vcode-app-id=%S\n" vcode-app-id)
      (sleep-for 0.1)
      )
    )
  (vr-log "**-- vcode-wait-for-handshake: exiting\n")
)

(defun vcode-send-kill-buffer ()
   "Sends a message to VCode server to tell it that Emacs has closed a buffer"
   (vr-log "-- vcode-send-kill-buffer: invoked")
   (let ((mess-cont (make-hash-table :test 'string=)))
     (cl-puthash "buff_name" (buffer-name) mess-cont)
     (cl-puthash "action" "close_buff" mess-cont)
     (vr-send-cmd 
       (run-hook-with-args 
	 'vr-serialize-message-hook (list "updates" mess-cont)))
   )
   (vr-log "-- vcode-send-kill-buffer: exiting")
)

(defun vcode-send-activate-buffer ()
   "Sends a message to VCode server to tell it that Emacs has voice activated
a buffer"
   (let ((mess-cont (make-hash-table :test 'string=)))
     (cl-puthash "buff_name" (buffer-name) mess-cont)
     (cl-puthash "action" "open_buff" mess-cont)
     (vr-send-cmd (list 'updates mess-cont))
   )
)

(defun vcode-send-activate-buffer ()
   "Sends a message to VCode server to tell it that Emacs has voice deactivated
a buffer"
   (let ((mess-cont (make-hash-table :test 'string=)))
     (cl-puthash "buff_name" (buffer-name) mess-cont)
     (cl-puthash "action" "close_buff" mess-cont)
     (vr-send-cmd (list 'updates mess-cont))
   )
)



(defun vcode-cmd-recognition-start (vcode-request)
  (vr-log "-- vcode-cmd-recognition-start: invoked\n")
  (let ((mess-cont (elt vcode-request 1)) 
	(resp-cont (make-hash-table :test 'string=)))

    ;;;
    ;;; Tell Emacs what the active window was when we heard the utterance
    ;;;
    (vr-cmd-frame-activated (list nil (cl-gethash 'window_id mess-cont)))

    ;;;
    ;;; Check if current buffer is speech enabled
    ;;;
    (if (vr-activate-buffer-p (current-buffer))
      (progn
	
        ;;;
        ;;; Reformulate the request received from VCode, into a request 
        ;;; that can be processed by the standard VR Mode function
        ;;;
	(vr-cmd-recognition (list nil 'begin))
	(cl-puthash "value" 1 resp-cont)
	)
      (cl-puthash "value" 0 resp-cont)
      )


    (vr-send-reply 
     (run-hook-with-args 
      'vr-serialize-message-hook (list "recog_begin_resp" resp-cont)))
    )

  (vr-log "-- vcode-cmd-recognition-start: exited\n")
    
  )


(defun vcode-cmd-recognition-end (vcode-request)
  (vr-log "-- vcode-cmd-recognition-end: invoked\n")
  (let ((empty-resp (make-hash-table :test 'string=)))
    ;;;
    ;;; Reformulate the request received from VCode, into a request 
    ;;; that can be processed by the standard VR Mode function
    ;;;
    (vr-cmd-recognition (list nil 'end))
    
    (vr-send-reply 
     (run-hook-with-args 
      'vr-serialize-message-hook (list "recog_end_resp" empty-resp)))
    )

  (vr-log "-- vcode-cmd-recognition-end: exited\n")

  )


(defun vcode-cmd-active-buffer-name (vcode-request)
  (vr-log "-- vcode-cmd-active-buffer-name: invoked\n")  
  (let ((mess-cont (make-hash-table :test 'string=)))
    (cl-puthash "value" (buffer-name) mess-cont)
    (vr-send-reply (run-hook-with-args 'vr-serialize-message-hook (list "active_buffer_name_resp" mess-cont)))
    )
  (vr-log "-- vcode-cmd-active-buffer-name: exited\n")  
  )

(defun vcode-serialize-changes (change-list)
  "Creates a change notification message to be sent to VCode speech server.

Argument 'change-list is a list of 5ple:
   (repl-start repl-end repl-length buffer-tick repl-text).
"

  (vr-log "-- vcode-serialize-changes: vr-changes-caused-by-sr-cmd=%S, change-list=%S\n" vr-changes-caused-by-sr-cmd change-list)
  (let ((mess "") (a-change) (repl-start) (repl-length) (repl-text)
	(change-list-vcode (list)) (a-change-vcode) (a-change-action)
	(mess-name) (mess-cont (make-hash-table :test 'string=)))

    (vr-log "**-- vcode-serialize-changes: after let\n")

    (while change-list

      ;;; Generate a hash describing this change and append it to the 
      ;;; change list destined for VCode
      (setq a-change (car change-list))
      (setq change-list (cdr change-list))
      (setq buff-name (nth 0 a-change))
      (setq repl-start (nth 1 a-change))

      ;;; For some reason, the overlay change notification reports one 
      ;;; characters too many for the region that was replaced with the
      ;;; changed text
      (setq repl-end (1- (nth 2 a-change)))
      (setq repl-length (nth 3 a-change))
      (setq repl-text (nth 5 a-change))

      (vr-log "**-- vcode-serialize-changes: serializing a-change=%S\n, buff-name=%S, repl-start=%S, repl-length=%S, repl-text=%S\n" a-change buff-name repl-start repl-length repl-text)

      (setq a-change-vcode (make-hash-table :test 'string=))
      (cl-puthash "range" 
		  (list repl-start repl-end) 
		  a-change-vcode)
      (cl-puthash "buff_name" buff-name a-change-vcode)
      (if (vr-change-is-delete repl-start repl-end repl-length)
	  (cl-puthash "action" "delete" a-change-vcode)
	(cl-puthash "action" "insert" a-change-vcode)
	(cl-puthash "text" repl-text a-change-vcode)
      )

      (vr-log "**-- vcode-serialize-changes: before range\n")

      (vr-log "**-- vcode-serialize-changes: before append, a-change-vcode=%S\n" a-change-vcode )
      (setq change-list-vcode 
	    (append change-list-vcode (list a-change-vcode)))
      (vr-log "**-- vcode-serialize-changes: after append, change-list-vcode=%S\n" change-list-vcode)
      )
    
    ;;; Name the message that will be sent to VCode.
    ;;; Changes generated in response to VCode request "some_command"
    ;;; -> name = "some_command_resp"
    ;;;
    ;;; Changes not generated in response to a VCode request:
    ;;; -> name = "updates_cbk"
    (if vr-changes-caused-by-sr-cmd
	(progn
	  (vr-log "**-- vcode-serialize-changes: non-nil vr-changes-caused-by-sr-cmd=%S\n" vr-changes-caused-by-sr-cmd)
	  (setq mess-name (format "%s_resp" vr-changes-caused-by-sr-cmd))
	  (vr-log "**-- vcode-serialize-changes: mess-name='%S'\n" mess-name)
	)
      (vr-log "**-- vcode-serialize-changes: nil vr-changes-caused-by-sr-cmd\n")
      (setq mess-name "updates_cbk")
      )
    (vr-log "**-- vcode-serialize-changes:  before puthash value\n")
    (cl-puthash "updates" change-list-vcode mess-cont)
    (vr-log "**-- vcode-serialize-changes: before serialize change-list-vcode=%S\n" change-list-vcode)

    (run-hook-with-args 
      'vr-serialize-message-hook (list mess-name mess-cont)))
)

(defun vcode-cmd-open-file (vcode-request)
  (vr-log "-- vcode-cmd-open-file: invoked\n")
  (let ((mess-cont (elt vcode-request 1)) 
	(file-name)
	(response (make-hash-table :test 'string=)))
    (vr-log "**-- vcode-cmd-open-file: before find-file\n")
    (setq file-name (cl-gethash "file_name" mess-cont))
    (vr-log "**-- vcode-cmd-open-file: file-name=%s\n" file-name)
    (find-file (substitute-in-file-name file-name))
    (cl-puthash "buffer_id" (buffer-name) response)
    (vr-log "**-- vcode-cmd-open-file: after find-file\n")
    (vr-send-reply
     (run-hook-with-args 
      'vr-serialize-message-hook (list "open_file_resp" response))
    )
  )
  (vr-log "-- vcode-cmd-open-file: exited\n")
)


(defun vcode-cmd-confirm-buffer-exists (vcode-request)
  (vr-log "-- vcode-confirm-buffer-exists: invoked\n")
  (let ((mess-cont (elt vcode-request 1)) 
	(buffer-name)
	(response (make-hash-table :test 'string=)))

    (setq buffer-name (cl-gethash "buff_name" mess-cont))
    (if (get-buffer buffer-name)
	(cl-puthash "value" 1 response)
      (cl-puthash "value" 0 response))
    (vr-send-reply
     (run-hook-with-args 
      'vr-serialize-message-hook (list "confirm_buffer_exists_resp" response))
    )
  )
  (vr-log "-- vcode-confirm-buffer-exists: exited\n")
)

(defun vcode-cmd-list-open-buffers (vcode-request)
  (vr-log "-- vcode-cmd-list-open-buffers: invoked\n")
  (let ((mess-cont (elt vcode-request 1)) 
	(open-buffers (buffer-list))
	(buffer-names nil)
	(response (make-hash-table :test 'string=)))

    (while open-buffers
      (append buffer-names (list (buffer-name (car open-buffers))))
      (setq open-buffers (cdr open-buffers))
      )

    (cl-puthash "value" buffer-names response)
    (vr-send-reply
     (run-hook-with-args 
      'vr-serialize-message-hook (list "confirm_buffer_exists_resp" response))
    )
  )
  (vr-log "-- vcode-cmd-list-open-buffers: exited\n")
)

(defun vcode-cmd-file-name (vcode-request)
  (vr-log "-- vcode-cmd-file-name: invoked\n")
  (let ((mess-cont (elt vcode-request 1)) 
	(response (make-hash-table :test 'string=))
	(buff-name) (file-name) (buff-name))
    (setq buff-name (cl-gethash "buff_name" mess-cont))
    (vr-log "**-- vcode-cmd-file-name: buff-name=%s\n" buff-name)
    (setq file-name (buffer-file-name (get-buffer buff-name)))
    (cl-puthash "value" file-name response)
    (vr-send-reply
     (run-hook-with-args 
      'vr-serialize-message-hook (list "file_name_resp" response))
    )
  )
  (vr-log "-- vcode-cmd-file-name: exited\n")
)



(defun vcode-cmd-close-buffer (vcode-request)
  (vr-log "-- vcode-cmd-close-buffer: invoked\n")
  (let ((mess-cont (elt vcode-request 1))
	(response (make-hash-table :test 'string=))
	(buff-name) (buff))

    (cl-puthash "value" 1 response)

    (setq buff-name (cl-gethash "buff_name" mess-cont))
    (setq buff (get-buffer "buff_name"))

    (if (not buff)
       ;;; 'buff_name is not the name of a buffer. Maybe the name
       ;;; of a file visited by a buffer?
	(setq buff (find-buffer-visiting buff-name))
      )

    (if buff
	(kill-buffer buff-name)
      ;;; No such buffer
      (ding) 
      (message (format "VR Mode: could not close buffer \"%S\"" buff-name))
      (cl-puthash "value" 0 response)
      )

    (vr-send-reply
     (run-hook-with-args 
      'vr-serialize-message-hook (list "close_buffer_resp" response))
    )

  (vr-log "-- vcode-cmd-close-buffer: exited\n")
  )
)

(defun vcode-cmd-language-name (vcode-request)
  (vr-log "WARNING: function vcode-cmd-language-name not implemented!!!\n")
  )

(defun vcode-fix-pos (pos)

  "Fixes a cursor position received from VCode server. 

If the position is nil, then returns the current position in the current 
buffer.

Also converts from VCode's 0-based positions to Emacs 1-based positions."

  (if (not pos) (setq pos (point))
    ;;; Only convert position if it was not nil (i.e. if we actually received
    ;;; it from VCode)
    (setq pos (vcode-convert-pos pos 'emacs)))
  pos
)

(defun vcode-fix-range (range)
  "Fixes a position range received from VCode server. This range
may contain nil or string values, and the 1st element may be
greater than the 2nd element."

  (vr-log "-- vcode-fix-range: invoked\n")
  (let ((start (nth 0 range)) (end (nth 1 range)) (tmp))
    (setq start (wddx-coerce-int start))
    (setq end (wddx-coerce-int end))

    ;;; Note: we set 'start and 'end to VCode's 0-based counting because
    ;;; they will later on be converted to Emacs 1-based counting
    (if (not start) (setq start 0))

    (if (not end) (setq end (buffer-size)))
    (setq start (vcode-convert-pos start 'emacs))
    (setq end (vcode-convert-pos end 'emacs))
    (if (> start end)
	(progn
	  (setq tmp end)
	  (setq end start)
	  (setq start end)
	  )      
      )
    (vr-log "-- vcode-fix-range: exiting with start=%S, end=%S\n" start end)
    (list start end)
  )
)

(defun vcode-convert-pos (pos for-who)
  "Because Emacs and VCode use a different base for counting character 
positions (Emacs starts from 1, VCode from 0), we need to convert from one
to the other"

;  (vr-log "-- vcode-convert-pos: invoked, pos=%s, for-who=%s\n" pos for-who)
  (if (equal for-who 'vcode)
      (1- pos)
    (1+ pos)
    )
)

(defun vcode-convert-range (start end for-who)
  (list (vcode-convert-pos start for-who) (vcode-convert-pos end for-who))
)

(defun vcode-make-sure-no-nil-in-selection (start end)
  "Makes sure that the selection is not 'nil"
  (if (not start) (setq start end))
  (if (not end) (setq end start))
  (list start end)
)

(defun vcode-cmd-cur-pos (vcode-request)
  (vr-log "-- vcode-cmd-cur-pos: invoked\n")
  (let ((mess-cont (make-hash-table :test 'string=)))
    (cl-puthash 'value (vcode-convert-pos (point) 'vcode) mess-cont)
    (vr-send-reply 
     (run-hook-with-args 
      'vr-serialize-message-hook (list "cur_pos_resp" mess-cont)))
    )
  (vr-log "-- vcode-cmd-cur-pos: exited\n")
  )

(defun vcode-cmd-line-num-of (vcode-request)
  (vr-log "-- vcode-cmd-line-num-of: invoked\n")
  (let ((mess-cont (nth 1 vcode-request))
	(response (make-hash-table :test 'string=))
	(line-num) (o-point))

    (vr-log "**-- vcode-cmd-line-num-of: before setq opoint\n")
    (setq opoint (vcode-fix-pos (cl-gethash "pos" mess-cont)))
    (vr-log "**-- vcode-cmd-line-num-of: after setq opoint=%S\n" opoint)

    (save-excursion
      (goto-char opoint)
      (beginning-of-line)
      (setq line-num (count-lines 1 (point)))
      )

    (vr-log "**-- vcode-cmd-line-num-of: after count-lines\n")
    (cl-puthash "value" line-num response)
    (vr-log "**-- vcode-cmd-line-num-of: before vr-send-reply\n")
    (vr-send-reply 
     (run-hook-with-args 
      'vr-serialize-message-hook (list "line_num_of_resp" response)))
    )
  (vr-log "-- vcode-cmd-line-num-of: exited\n")
  )


(defun vcode-cmd-get-selection (vcode-request)
  (vr-log "-- vcode-cmd-get-selection: invoked\n")
  (let ((response (make-hash-table :test 'string=))
	(selection))
    (setq selection (vcode-make-sure-no-nil-in-selection (point) (mark)))
    (cl-puthash 'value 
		(list (vcode-convert-pos (nth 0 selection) 'vcode)
		      (vcode-convert-pos (nth 1 selection) 'vcode))
		response)
    (vr-send-reply 
     (run-hook-with-args 
      'vr-serialize-message-hook (list "get_selection_resp" response)))
    )
  (vr-log "-- vcode-cmd-get-selection: exited\n")
  )

(defun vcode-cmd-get-text (vcode-request)
  (vr-log (format "-- vcode-cmd-get-text: invoked, vcode-request=%S\n" vcode-request))
  (let ((mess-cont (make-hash-table :test 'string=)) 
	(vcode-request-cont (elt vcode-request 1))
	(start) (end)
	)
    (vr-log "**-- vcode-cmd-get-text: before start\n")
    (setq start (wddx-coerce-int (cl-gethash "start" vcode-request-cont)))
    (setq end (wddx-coerce-int (cl-gethash "end" vcode-request-cont)))
    (setq fixed-range (vcode-fix-range (list start end)))
    (setq start )
    (setq end (nth 1 fixed-range))
   
    (vr-log "**-- vcode-cmd-get-text: before 'value, (type-of start)=%S, (type-of end)=%S, start=%S, end=%S\n" (type-of start) (type-of end) start end)
    (cl-puthash "value" (buffer-substring 
			  (nth 0 fixed-range) 
			  (nth 1 fixed-range)) mess-cont)
    (vr-log "**-- vcode-cmd-get-text: before 'send-reply\n")

    (vr-send-reply 
     (run-hook-with-args 
      'vr-serialize-message-hook (list "get_text_resp" mess-cont)))
    )
  (vr-log "-- vcode-cmd-get-text: exited\n")
  )


(defun vcode-cmd-get-visible (vcode-request)
  (vr-log "-- vcode-cmd-get-visible: invoked\n")
  (let ((mess-cont (make-hash-table :test 'string=)))
    (cl-puthash 'value (list (window-start) (window-end)) mess-cont)
    (vr-send-reply (run-hook-with-args 'vr-serialize-message-hook (list "get_visible_resp" mess-cont)))
    )  
  (vr-log "-- vcode-cmd-get-visible: exited\n")
  )

(defun vcode-cmd-len (vcode-request)
  (vr-log "-- vcode-cmd-len: invoked\n")
  (let ((mess-cont (make-hash-table :test 'string=)))
    (cl-puthash 'value (buffer-size) mess-cont)
    (vr-send-reply (run-hook-with-args 'vr-serialize-message-hook (list "get_visible_resp" mess-cont)))
    )  
  (vr-log "-- vcode-cmd-len: exited\n")
  )

(defun vcode-cmd-newline-conventions (vcode-request)
  (vr-log "-- vcode-cmd-newline-conventions: invoked\n")
  (let ((mess-cont (make-hash-table :test 'string=)))
    (cl-puthash 'value (list "\n") mess-cont)
    (vr-send-reply (run-hook-with-args 'vr-serialize-message-hook (list "newline_conventions_resp" mess-cont)))
    )  
  (vr-log "-- vcode-cmd-newline-conventions: exited\n")
  )

(defun vcode-cmd-pref-newline-conventions (vcode-request)
  (vr-log "-- vcode-cmd-pref-newline-conventions: invoked\n")
  (let ((mess-cont (make-hash-table :test 'string=)))
    (cl-puthash 'value "\n" mess-cont)
    (vr-send-reply (run-hook-with-args 'vr-serialize-message-hook (list "pref_newline_conventions_resp" mess-cont)))
    )  
  (vr-log "-- vcode-cmd-pref-newline-conventions: exited\n")
)

(defun vcode-generate-set-selection-updates (sel-start sel-end)
  (let ((upd-list nil) (a-change-vcode (make-hash-table :test 'string=)))
      (cl-puthash "range" 
		  (list sel-start sel-end) 
		  a-change-vcode)
      (cl-puthash "buff_name" (buffer-name) a-change-vcode)
      (vr-log "-- vcode-generate-set-selection-updates: before puthash action")
      (cl-puthash "action" "select" a-change-vcode) 
      (vr-log "-- vcode-generate-set-selection-updates: after puthash action")
      (cl-puthash "range" (list sel-start sel-end) a-change-vcode)
      (cl-puthash "cursor_at" 1 a-change-vcode)
      a-change-vcode
  )
)

(defun vcode-cmd-set-selection (vcode-request)
  (vr-log "-- vcode-cmd-set-selection: invoked\n")
  (let ((mess-cont (elt vcode-request 1))
       (sel-range) (put-cursor-at) (sel-start) (sel-end)
       (reply-cont (make-hash-table :test 'string=)))
    (setq sel-range (cl-gethash "range" mess-cont))
    (setq put-cursor-at (cl-gethash "cursor_at" mess-cont))
    (if (= put-cursor-at 1) 
	(progn 
	  (setq sel-start (elt sel-range 0))
	  (setq sel-end (elt sel-range 1))
	  )
      (progn 
	(setq sel-start (elt sel-range 1))
	(setq sel-end (elt sel-range 0))
	)
      )
    (goto-char sel-start)
    (set-mark sel-end)
    (cl-puthash "updates" (vcode-generate-set-selection-updates 
			   sel-start sel-end)
		reply-cont)
    (vr-send-reply (run-hook-with-args 
		    'vr-serialize-message-hook 
		    (list "set_selection_resp" reply-cont)))
  )
)

(defun vcode-cmd-move-relative-page (vcode-request)
  (vr-log "-- vcode-cmd-move-relative-page: invoked\n")
  (let ((mess-cont (elt vcode-request 1)) (direction) (num))
    (setq direction (cl-gethash "direction" mess-cont))
    (setq num (cl-gethash "num" mess-cont))
    (if (>= direction 0)
	(scroll-down-nomark num)
      (scroll-up-nomark num))
  )
  (vr-log "-- vcode-cmd-move-relative-page: exited\n")
)

(defun vcode-cmd-insert (vcode-request)
  (vr-log "-- vcode-cmd-insert: invoked\n")
  (let ((mess-name (elt vcode-request 0)) 
	(mess-cont (elt vcode-request 1))
	(text) (range) (vr-request) 
	(repl-start) (repl-end))

	(setq text (cl-gethash "text" mess-cont))
	(setq range (vcode-fix-range (cl-gethash "range" mess-cont)))
	(setq repl-start (elt range 0))
	(setq repl-end (elt range 1))

        (vr-log "--** vcode-cmd-insert: text='%S', range=%S, repl-start=%S, repl-end=%S\n" text range repl-start repl-end)

	(setq vr-request (list repl-start
			       (- repl-end repl-start)
			       text
			       (+ repl-start (length text))
			       0
			       1
			       0
			       mess-name
			       ))
        (vr-log "--** vcode-cmd-insert: vr-request=%S\n" vr-request)

	(vr-cmd-make-changes vr-request)
    )
  (vr-log "-- vcode-cmd-insert: exited\n")
  )

(defun vcode-cmd-indent (vcode-request)
  (vr-log "-- vcode-cmd-indent: invoked\n")
  (let ((mess-name (elt vcode-request 0)) 
	(mess-cont (elt vcode-request 1))
	(range) (vr-request) 
	(indent-start) (indent-end))

	(setq range (vcode-fix-range (cl-gethash "range" mess-cont)))
	(vr-log "--** vcode-cmd-indent: range=%S\n" range)
	(setq indent-start (elt range 0))
	(setq indent-end (elt range 1))

        (vr-log "--** vcode-cmd-indent: indent-start=%S, indent-end=%S\n"  indent-start indent-end)

	(setq vr-request (list 1
			       0
			       ""
			       (point)
			       0
			       indent-start
			       (- indent-end indent-start)
			       mess-name))
        (vr-log "--** vcode-cmd-indent: vr-request=%S\n" vr-request)

	(vr-cmd-make-changes vr-request)
    )
  (vr-log "-- vcode-cmd-indent: exited\n")
  )

(defun vcode-cmd-decr-indent-level (vcode-request)
  (vr-log "-- vcode-cmd-decr-indent-level: NOT IMPLEMENTED YET!!!\n")
  (let ((mess-name (elt vcode-request 0)) 
	(mess-cont (elt vcode-request 1))
	(range) (vr-request) 
	(indent-start) (indent-end))

	(setq range (vcode-fix-range (cl-gethash "range" mess-cont)))
	(setq indent-start (elt range 0))
	(setq indent-end (elt range 1))
	(setq vr-request (list 1
			       0
			       ""
			       (point)
			       0
			       indent-start
			       (- indent-end indent-start)
			       1
			       ??? est-ce que mess-name est a la bonne
			       ??? position pour vr-request?
			       mess-name))

  )
)

(defun vcode-unindent-region (start end n-levels)
  "Deindents region from START to END by N-LEVELS levels."
  (let (end-line)
    (vr-log "-- vcode-unindent-region: start=%S, end=%S, n-levels=%S" start end n-levels)
    (save-excursion
      (goto-char end)
      (setq end-line (count-lines 1 (point)))
      (message "-- end-line=%S\n" end-line)
      (goto-char start)
      (while (<= (count-lines 1 (point)) end-line)
 	(message "-- start of while, current-line=%S" (count-lines 1 (point)))
  	(vcode-unindent-line n-levels)
	(next-line 1)
 	(message "-- end of while, current-line=%S" (count-lines 1 (point)))
       )
    )
  )
)


(defun vcode-unindent-line (n-levels)
  (interactive "nNumber of levels: ")
  (beginning-of-line)
  (while (and (looking-at " ") (< (point) (point-max)))
    (forward-char-nomark 1)
    )

  ;;; Will need to invoke a different method for different languages
  ;;; Or maybe, we can just invoke whatever function is bound to the 
  ;;; Backspace key
  ;;;
  ;;; Don't backsapce if empty line, because that will delete the line 
  ;;; instead of deindenting
  ;;;
  (if (not (looking-at "$"))
      (progn
	(vr-log "--** vcode-unindent-line: unindenting line")
	(py-electric-backspace 1)
	)
    (vr-log "--** vcode-unindent-line: line was blank... leave it alone")
    )
)


(defun vcode-cmd-unindent (vcode-request)
  (vr-log "WARNING: function vcode-cmd-unindent not implemented!!!\n")
)

(defun vcode-cmd-delete (vcode-request)
  (vr-log "WARNING: function vcode-cmd-delete not implemented!!!\n")
  )

(defun vcode-cmd-goto (vcode-request)
  (vr-log "-- vcode-cmd-goto: invoked\n")
  (let ((mess-cont (elt vcode-request 1))
       (pos) (response (make-hash-table :test 'string=)) 
       (goto-update (make-hash-table :test 'string=)))

    (setq pos (cl-gethash "pos" mess-cont))
    (condition-case err     
	 (goto-char (vcode-fix-pos pos))
       ('error (error "VR Error: could not go to position %S" pos)))      

     ; Send back an update describing where we actually went, not where we 
     ; meant to go
     (setq pos (cl-gethash "pos" mess-cont))
     (cl-puthash "buff_name" (buffer-name) goto-update)
     (cl-puthash "action" "goto" goto-update)
     (cl-puthash "pos" (vcode-convert-pos (point) 'vcode) goto-update)
     (cl-puthash "updates" (list goto-update) response)
     (vr-send-reply 
      (run-hook-with-args 
       'vr-serialize-message-hook (list "goto_resp" response)))

     (vr-log "-- vcode-cmd-goto: exited\n")  
  )
)

