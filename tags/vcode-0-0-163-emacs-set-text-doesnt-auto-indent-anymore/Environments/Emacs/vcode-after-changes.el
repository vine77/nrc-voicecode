;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; New of vc.el which uses after-change-functions which is much simpler and
;; more robust than overlays as per Barry Jaspan's vr.el
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;
;; Vcode Mode - integration of GNU Emacs and VoiceCode 
;;    http://voicecode.iit.nrc.ca/VoiceCode
;;
;; Based on VR Mode by Barry Jaspan
;;
;; Copyright 1999 Barry Jaspan, <bjaspan@mit.edu>.  All rights reserved.
;;
;; $Id: vc.el,v 1.9 2002/08/05 22:59:58 alain_desilets Exp $
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

;;; Change this if you want to see more traces
(setq message-log-max 10000)

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
(setq vr-log-do nil)

(defvar vcode-traces-on (make-hash-table :test 'string=)
"Set entries in this hashtable, to activate traces with that name.")
;(cl-puthash "vr-execute-event-handler" 1 vcode-traces-on)
;(cl-puthash "vcode-cmd-get-text" 1 vcode-traces-on)
;(cl-puthash "vcode-cmd-set-text" 1 vcode-traces-on)
;(cl-puthash "vcode-execute-command-string" 1 vcode-traces-on)

(defvar vr-log-send nil "*If non-nil, VR mode logs all data sent to the VR
subprocess in the 'vr-log-buff-name buffer.")

(defvar vr-log-read nil "*If non-nil, VR mode logs all data received
from the VR subprocess in the 'vr-log-buff-name buffer.")

(defvar vr-log-buff-name "*Messages*" "Name of the buffer where VR log messages are 
sent."
)
(setq message-log-max 100000)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Code for running in testing mode
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defun vcode-close-all-buffers ()
   (interactive)
   (let ((all-buffs (buffer-list)) (curr-buffer))
     (while all-buffs
       (setq curr-buffer (car all-buffs))
       (message "-- curr-buffer=%S, (buffer-name curr-buffer)=%S" curr-buffer (buffer-name curr-buffer))
       (setq all-buffs (cdr all-buffs))
       (kill-buffer curr-buffer)
     )
   )
)

(defun vcode-test ()
  (interactive)
  (setq debug-on-error t)
  (setq debug-on-quit t)
 
  (vcode-close-all-buffers)
  (setq vr-activation-list (list "\.py$" "\.c$" "\.cpp$" "\.h$"))
  (vcode-configure-for-regression-testing t)
  (vr-mode 1 "vcode-test")
;  (vcode-configure-for-regression-testing nil)
;  (vr-mode nil)
)

(defun vcode-config-py-mode-for-regression-testing ()
   (setq py-smart-indentation nil) 
   (setq py-indent-offset 3)
   (setq tab-width 999)
)

(defun vcode-configure-for-regression-testing (status)
   (if status
       (progn 
	 (add-hook 'python-mode-hook 
		   'vcode-config-py-mode-for-regression-testing)
       )
     (remove-hook 'python-mode-hook 
		   'vcode-config-py-mode-for-regression-testing)
   )
)



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

(defvar vr-process nil "The VR mode subprocess.")

(defvar vr-emacs-cmds nil "The socket connection used to send messages 
initiated by Emacs, and to get responses from the SR server.")

(defvar vr-dns-cmds nil "The socket connection used to receive messages
initiated by the SR server, and to send replies to them.
")

(defvar vr-reading-string nil "Storage for partially-read commands
from the VR subprocess.")

(defvar vr-buffer nil "The current voice-activated buffer, or nil.
See vr-activate-buffer and vr-switch-to-buffer.")

(defvar vr-ignore-changes nil "see comment in vr-overlay-modified")
(defvar vr-changes-caused-by-sr-cmd nil "see comment in vr-report-insert-delete-change")
(defvar vr-queued-changes nil "see comment in vr-report-insert-delete-change")
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
  (vr-log "--** vr-post-command: invoked\n")
  (add-hook 'post-command-hook 'vr-post-command)
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
	))
  (vr-log "--** vr-post-command: exited\n")
)

(defun vr-kill-buffer ()
  (if (vr-activate-buffer-p (current-buffer))
      (progn
	(run-hooks 'vr-send-kill-buffer-hook)
	)
    )
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
;  (vr-log "--** vr-maybe-activate-buffer: invoked\n")
  (if (and (not isearch-mode) (vr-activate-buffer-p (buffer-name buffer)))
      (if (eq buffer vr-buffer)
	  nil
	(vr-activate-buffer buffer))
    (if vr-buffer 
	(vr-activate-buffer nil)))
;  (vr-log "--** vr-maybe-activate-buffer: exited\n")
)

(defun vr-switch-to-buffer ()
  "Select the current VR mode target buffer in the current window."
  (interactive)
  (if (buffer-live-p vr-buffer)
      (switch-to-buffer vr-buffer)
    (error "VR target buffer no longer exists; use vr-activate-buffer")))



(defun vcode-set-after-change-functions (status)
  (vr-log "--** vcode-set-after-change-functions: invoked, (current-buffer)=%S, status=%S\n" (current-buffer) status)
  (if status
      (progn
;	(make-local-hook 'after-change-functions)
	(add-hook 'after-change-functions 'vr-report-insert-delete-change)
	)
    (remove-hook 'after-change-functions 'vr-report-insert-delete-change)
    )
  (vr-log "--** vcode-set-after-change-functions: upon exit, (current-buffer)=%S, after-change-functions=%S\n" (current-buffer) after-change-functions)  
)

(defun vr-activate-buffer (buffer)
  "Sets the target BUFFER that will receive voice-recognized text.  Called
interactively, sets the current buffer as the target buffer."
  (interactive (list (current-buffer)))
  (if (buffer-live-p vr-buffer)
      (save-excursion
	(set-buffer vr-buffer)
	(kill-local-variable 'vr-mode-line)))
  (set-default 'vr-mode-line (concat " VR-" vr-mic-state))
  (setq vr-buffer buffer)
  (if buffer
      (save-excursion
	(set-buffer buffer)
	(setq vr-mode-line (concat " VR:" vr-mic-state))
	(run-hooks 'vr-send-activate-buffer)
	)
    (run-hooks 'vr-send-deactivate-buffer)
    )
  (force-mode-line-update)
  )

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Tracking changes to voice-activated buffers
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


(defvar vr-modification-stack () )


(defun vr-change-is-delete (beg end &optional len)
  (and (> len 0) (eq beg end))
)

(defun vr-change-is-self-insert (beg end &optional len)
  (and (eq len 0) 
       (eq (- end beg) 1) 
       (eq (char-after beg) last-command-char))
)

(defun vr-execute-deferred-function ()
  (if deferred-function
      (progn
	(setq vr-deferred-deferred-function deferred-function)
	(setq deferred-function nil)
	(delete-backward-char 2)
	(fix-else-abbrev-expansion)
	(if (not (eq vr-deferred-deferred-function
		     'else-expand-placeholder))
	    (progn
	      ;;(call-interactively deferred-deferred-function)
	      (setq vr-deferred-deferred-deferred-function
		    vr-deferred-deferred-function )
	      (setq vr-deferred-deferred-function nil)
	      (vr-execute-command
	       vr-deferred-deferred-deferred-function))

	  )
	))
)


(defun vr-report-insert-delete-change (inserted-start inserted-end deleted-len)
  "Invoked whenever an insertion or deletion change happens on the current 
buffer (if it is voice enabled). 

Changes are put in a changes queue `vr-queued-changes.

If 'vr-changes-caused-by-sr-cmd is nil, the changes were not
done as a response to a voice command. In that case, send the 
queued message right away.

If 'vr-changes-caused-by-sr-cmd not nil, the changes have
been generated by a command from the SR server. In that case,
leave the messages in the queue. The event handler for that command
will send the queued changes as a big reply message, when it's done
executing.
"

  (let ((the-change nil))
    (if (vr-activate-buffer-p (current-buffer))
	(progn 
	  (vr-log "--** vr-report-insert-delete-change: inserted-start=%S inserted-end=%S deleted-len=%S\n" inserted-start inserted-end deleted-len)
	  (setq the-change
		(vr-generate-raw-change-description 'change-is-insert (list (buffer-name) inserted-start inserted-end deleted-len))
		)
	  
	  (vr-log "--** vr-report-insert-delete-change: the-change=%S" the-change)
	  
	  (setq vr-queued-changes (cons the-change vr-queued-changes))
	  
	  (if (not vr-changes-caused-by-sr-cmd)
	      (vr-send-queued-changes)
	    )
	  
	  ;;
	  ;; What does this do? Is it still necessary if we disable dabbrevs
	  ;; and electric punctuation marks during executio of utterances?
	  (vr-execute-deferred-function)
       )
    )
  )
)


(defun vr-report-goto-select-change (buff-name sel-start sel-end)
  "Invoked whenever a change in the cursor position or marked selection 
happens on a buffer (if it is voice enabled). 

Changes are put in a changes queue `vr-queued-changes.
"
  (setq vr-queued-changes 
	(cons 
;	   (list 'change-is-select buff-name sel-start sel-end)
	   (vr-generate-raw-change-description  'change-is-select (list buff-name sel-start sel-end))
	   vr-queued-changes))
)

(defun vr-generate-raw-change-description (change-type change-data)

  (let ((change-desc) (buff-name) (inserted-start) (inserted-end) 
	(deleted-length) (deleted-start) (deleted-end) (inserted-text))
    (if (eq 'change-is-select change-type)
	(progn 
	  (setq change-desc (list change-type change-data))
	)
      (setq buff-name (nth 0 change-data))
      (setq inserted-start (nth 1 change-data))
      (setq inserted-end (nth 2 change-data))
      (setq deleted-length (nth 3 change-data))	
      (setq deleted-start inserted-start)
      (setq deleted-end (+ deleted-start deleted-length))
      (save-excursion
	(switch-to-buffer buff-name)
	(setq inserted-text (buffer-substring inserted-start inserted-end))
      )
      (setq change-desc (list change-type (list buff-name deleted-start deleted-end inserted-text)))
    )
    change-desc
  )
)

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

(defun vcode-trace (trace-name format-string &rest s)
   (let ((buf) (win))
     (setq buf (get-buffer-create vr-log-buff-name))
     (setq win (get-buffer-window buf 't))
     (if (or (not trace-name) (is-in-hash trace-name vcode-traces-on))
        (progn
          (setq format-string (concat "-- " trace-name ": " format-string "\n"))
          (save-excursion
            (set-buffer buf)
            (goto-char (point-max))

            (if s
                (insert (apply 'format (append (list format-string) s)))
              (insert format-string)
              )
            (if win
                (set-window-point win (point-max)))
           )
        )
     )
   )
)
 
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
 	  (let ((this-command cmd))
	    (run-hooks 'post-command-hook)))
  t)

(defun vcode-execute-command-string (command-string)
  "Execute a string as though it was typed by the user.
"
  (let ()
    (vcode-trace "vcode-execute-command-string" "upon entry, (current-buffer)=%S, py-indent-offset=%S, tab-width=%S, command-string=%S, (point)=%S, (mark)=%S, after-change-functions=%S buffer is\n%S" (current-buffer) py-indent-offset tab-width command-string (point) (mark) after-change-functions (buffer-substring (point-min) (point-max)))
    (setq debug-on-error t)
    (setq debug-on-quit t)

    ;;
    ;; Convert the string to a list of Emacs events
    ;;
    (setq unread-command-events
	  (append unread-command-events
		  (listify-key-sequence command-string)))

    ;;;
    ;;; Execute each event
    ;;;
    (while unread-command-events
      (let* ((event (read-key-sequence-vector nil))
 	     (command (key-binding event))
 	     (last-command-char (elt event 0))
 	     (last-command-event (elt event 0))
 	     (last-command-keys event)
 	     )
	(vcode-trace "vcode-execute-command-string" "command=%S" command)
	(run-hooks 'pre-command-hook)
	(command-execute command nil )
	(run-hooks 'post-command-hook)
      )
    )
  )
)



(defun vr-send-queued-changes ()
  "Sends the message queue.

   If 'vr-changes-caused-by-sr-cmd is not nil, then these changes happened
   in response to a SR command (and 'vr-changes-caused-by-sr-cmd is the name
   of that command)."

  (let ((change-message nil))

    (setq change-message
       (run-hook-with-args 'vr-serialize-changes-hook
			   (nreverse vr-queued-changes)))

    ;;;
    ;;; If these changes happened in response to a command, send them on 
    ;;; the reply channel.
    ;;; Otherwise, send them on the cmd channel.
    ;;;
    (if vr-changes-caused-by-sr-cmd
	(vr-send-reply change-message)
      (vr-send-cmd change-message)
    )
    (setq vr-queued-changes nil)
  )
)

(defun vr-execute-event-handler (handler vr-request)
  (let ((vr-changes-caused-by-sr-cmd (nth 0 vr-request))
	(vr-request-mess (nth 1 vr-request)))
    (vr-log "**-- vr-execute-event-handler: vr-changes-caused-by-sr-cmd=%S\n" vr-changes-caused-by-sr-cmd)

    ;;;
    ;;; Fix the message arguments that refer to buffer positions
    ;;; (Emacs counts from 1 while VCode counts from 1, and VCode
    ;;; may send some nil positions)
    ;;;
    (setq vr-request 
	  (list vr-changes-caused-by-sr-cmd
		(vcode-fix-positions-in-message 
		 vr-request-mess 'emacs)
		))

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
    (setq vr-changes-caused-by-sr-cmd nil)
    )
)

		
(defun vr-output-filter (p s)
  (setq vr-reading-string (concat vr-reading-string s))
  (while (> (length vr-reading-string) 0)
    (let* ((handler) 
	   (parsed (condition-case err
 		       (run-hook-with-args 
			   'vr-deserialize-message-hook vr-reading-string)
		     ('end-of-file (error "Invalid VR command received: %s"
					  vr-reading-string))))
	   (vr-request (elt parsed 0))
	   (idx (elt parsed 1))
	   (vr-cmd (elt vr-request 0)))
      (setq vr-reading-string 
	    (if (< idx (1- (length vr-reading-string)))
		(substring vr-reading-string (1+ idx))
	       ""))

      (setq handler (cl-gethash vr-cmd vr-message-handler-hooks))
      (if handler
	  (vr-execute-event-handler handler vr-request)

 	;; The VR process should fail gracefully if an expected
 	;; reply does not arrive...
 	(error "Unknown VR request: %s" vr-request))
    )
  )
)
     

(defun vr-send-reply (msg)
  (if (and vr-dns-cmds (eq (process-status vr-dns-cmds) 'open))
      (progn
	(if (integerp msg)
	    (setq msg (int-to-string msg)))
	(if vr-log-send
	    (vr-log "<- r %s\n" msg))
;;; Alain what does that do? Should it be part of vr-serialize-message?
;;; 	(process-send-string vr-dns-cmds (vr-etonl (length msg)))

	(process-send-string vr-dns-cmds msg))
    (message "VR Mode DNS reply channel is not open!"))
  )

(defun vr-send-cmd (msg)
  (if (and vr-emacs-cmds (eq (process-status vr-emacs-cmds) 'open))
      (progn
	(if vr-log-send
	    (vr-log "<- c %s\n" msg))
;;; Should this be part of vr-serialize-message???
;;;	(process-send-string vr-emacs-cmds (vr-etonl (length msg)))

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
  (condition-case e
      (progn
 	(setq vr-emacs-cmds (open-network-stream "vr-emacs" nil
 						 host port))

	;;;
	;;; Connect an output filter to the Emacs commands network-stream
	;;; in case the speech server needs to to some handshaking on that
	;;; connection.
	;;;
	(set-process-filter vr-emacs-cmds 'vr-output-filter)
	(vr-log "connecting to speech server %s\n" vr-emacs-cmds)
	
	;;;
	;;; Possibly wait until Emacs has shaken hands with speech server
	;;; before opening second network stream.
	;;;
	(run-hooks 'vr-wait-for-handshake-hook)

	(setq vr-dns-cmds (open-network-stream "vr-dns" nil host (1+ port)))
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
server to configure VR Mode for (either 'vr,  'vcode, or 'vcode-test). 

If not specified,
use whatever speech server VR Mode is currently configured for.

VR mode supports Dragon NaturallySpeaking dictation, Select 'N
Say(tm), and voice commands in Emacs buffers.  See README.txt for
instructions.

\\{vr-map}"
 (interactive "P")

  (setq vr-vcode-test-client 0)
  (if speech-server
    (cond
      ((string= speech-server "vr") (vr-mode-configure-for-vr-server))
      ((string= speech-server "vcode") (vr-mode-configure-for-vcode-server))
      ((string= speech-server "vcode-test") (setq vr-vcode-test-client 1) (vr-mode-configure-for-vcode-server))
      
    )
  )

  (vr-mode-activate arg)
)

(defun vr-mode-activate (arg)
  "Activates the VR mode, after it has been configured for a particular
speech server"

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
	(vcode-set-after-change-functions 1)
	)
    
    ;; Leaving VR mode
    (remove-hook 'post-command-hook 'vr-post-command)
    (remove-hook 'minibuffer-setup-hook 'vr-enter-minibuffer)
    (remove-hook 'kill-buffer-hook 'vr-kill-buffer)
    (vr-activate-buffer nil)
    (if vr-host
	(vr-sentinel nil "finished\n")
      (vr-send-cmd "exit"))
    (vcode-set-after-change-functions nil)
    (run-hooks 'vr-mode-cleanup-hook)
    )
 (force-mode-line-update)
)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Configuration allowing vr-mode to interact with the VR.exe speech
;;; server.
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defun vr-deserialize-message (message)
   "Parse a message serialized send by VR.exe as a sexp."

   (read-from-string message)
)

(defun vr-serialize-message (message)
  "Serialises a LISP data structure into a message that can be parsed by
   VR.exe" 

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
    cmd
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
     (vr-send-cmd  (concat "kill-buffer " (buffer-name (current-buffer))))
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


(defun vr-cmd-frame-activated (wnd)

  ;; This is ridiculous, but Emacs does not automatically change its
  ;; concept of "selected frame" until you type into it.  So, we have
  ;; the subprocess send us the HWND value and explcitly activate the
  ;; frame that owns it.  The HWND may not belong to any frame, for
  ;; example if vr-win-class/title match a Windows window not
  ;; belonging to Emacs.  In that case, just ignore it.
  ;;
  (let* ((frame (car (vr-filter
		      (lambda (f) (equal (cdr (assoc 'window-id
						     (frame-parameters f)))
					 wnd))
		      (visible-frame-list)))))

    (if frame
	(select-frame frame)
      (message "VR Mode: %s is not an Emacs frame window handle; ignored."
	       wnd)))
  (vr-maybe-activate-buffer (current-buffer))

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


;; This function is called by Dragon when it begins/ends mulling over an
;; utterance; delay key and mouse events until it is done.  This
;; ensures that key and mouse events are not handled out of order
;; with respect to speech recognition events
(defun vr-cmd-recognition (vr-request)
  (let ((state (nth 1 vr-request)))
    (progn
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

(defvar vcode-instance-string nil
"Another unique ID assigned to this instance of Emacs."
)

(defun vcode-make-all-keys-self-insert ()
  
)

(defun vr-mode-configure-for-vcode-server ()
  "Configures VR Mode for interacting with the VoiceCode speech server."

  ;;;
  ;;; VCode will do automatic indentation and stuff.
  ;;;
  (vcode-make-all-keys-self-insert)

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
  (cl-puthash 'test_client_query 'vcode-cmd-test-client-query vr-message-handler-hooks)
  (cl-puthash 'set_instance_string 'vcode-cmd-set-instance-string vr-message-handler-hooks)
  (cl-puthash 'instance_string 'vcode-cmd-get-instance-string vr-message-handler-hooks)


  (cl-puthash 'suspendable 'vcode-cmd-suspendable 
	      vr-message-handler-hooks)
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
  (cl-puthash 'set_text 'vcode-cmd-set-text vr-message-handler-hooks)  
  (cl-puthash 'indent 'vcode-cmd-indent vr-message-handler-hooks)  
  (cl-puthash 'decr_indent_level 'vcode-cmd-decr-indent-level vr-message-handler-hooks)
  (cl-puthash 'delete 'vcode-cmd-delete vr-message-handler-hooks)  
  (cl-puthash 'goto 'vcode-cmd-goto vr-message-handler-hooks)  
  (cl-puthash 'goto_line 'vcode-cmd-goto-line vr-message-handler-hooks)  

  (cl-puthash 'mediator_closing 'vcode-cmd-mediator-closing vr-message-handler-hooks)  

  ;;;
  ;;; These ones are currently not handled by VCode, but they probably should
  ;;;
;  (cl-puthash 'heard-command 'vr-cmd-heard-command-hook vr-message-handler-hooks)
;  (cl-puthash 'mic-state 'vr-cmd-mic-state-hook vr-message-handler-hooks)



  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
  ;;; These messages are defined in VR.exe but don't seem useful for VCode.
  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


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


;;; Not needed in VCode. VCode will send different messages to make different
;;; kinds of changes.
;  (cl-puthash 'make-changes 'vr-cmd-make-changes vr-message-handler-hooks)

)


(defun vcode-serialize-message (mess)
  "Serializes a LISP data structure into a string message that can be sent to 
VoiceCode server."
  (let ((mess-name (elt mess 0)) (mess-cont (elt mess 1)))
    (setq serialized-mess (vcode-pack-mess (vcode-encode-mess mess-name mess-cont)))
    serialized-mess
  )
)

(defun vcode-deserialize-message (mess)
  "Deserializes a string message received from the VoiceCode server 
into a LISP data structure."

  (let ((unpack-result) (unpacked-mess) (bytes-parsed) 
	(mess-name) (mess-cont))

    ;;;
    ;;; Unpack the message
    ;;;
    (setq unpack-result (vcode-unpack-mess mess))
    (setq unpacked-mess (elt unpack-result 0))
    (setq bytes-parsed (elt unpack-result 1))

    ;;;
    ;;; Then decode it
    ;;; 
    (setq mess (vcode-decode-mess unpacked-mess ))
    (setq mess-name (elt mess 0))
    (setq mess-cont (elt mess 1))
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

(defun vcode-get-buff-name-from-message (message)
  "Returns name of \"buff_name\" element in 'message. If absent or nil, then
returns name of current buffer."
  (let ((buff-name (cl-gethash "buff_name" message nil)))
    (if (not buff-name)
	(setq buff-name (buffer-name (current-buffer)))
    )
    buff-name
  )
)

(defun vcode-cmd-send-app-name (vcode-req)
   "Sends the name of the application ('Emacs) to the VoiceCode server."


   (let ((mess-cont (make-hash-table :test 'string=)))
     (cl-puthash "value" "emacs" mess-cont)
     (vr-send-cmd (run-hook-with-args 'vr-serialize-message-hook (list "app_name" mess-cont)))
  )

)


(defun vcode-cmd-test-client-query (vcode-req)
   "Sends the name of the application ('Emacs) to the VoiceCode server."


   (let ((mess-cont (make-hash-table :test 'string=)))
     (cl-puthash "value" vr-vcode-test-client mess-cont)
     (vr-send-cmd (run-hook-with-args 'vr-serialize-message-hook (list "test_client_query_resp" mess-cont)))
  )

)

(defun vcode-cmd-set-instance-string (vcode-req)
   (let ((resp-cont (make-hash-table :test 'string=)))

   (setq vcode-instance-string (cl-gethash "instance_string" (nth 1 vcode-req)))
   (cl-puthash "value" vcode-instance-string resp-cont)

   (setq frame-title-format 
          `("%b -- " (,vcode-instance-string invocation-name "@" system-name)))

;   (setq frame-title-format 
;	 `(multiple-frames "%b" (,vcode-instance-string invocation-name "@" system-name)))

     (vr-send-reply (run-hook-with-args 
		   'vr-serialize-message-hook (list "set_instance_string_resp" resp-cont)))
  )

)

(defun vcode-cmd-get-instance-string (vcode-req)
   (let (resp-cont (make-hash-table :test 'string=))
     (cl-puthash "value"  vcode-instance-string resp-cont)
     (vr-send-reply (run-hook-with-args 
		   'vr-serialize-message-hook (list "get_instance_string_resp" resp-cont)))
  )

)

(defun vcode-cmd-your-id-is (vcode-req)
   "Stores the unique ID assigned by VoiceCode to this instance of Emacs, so 
we can send it back to VoiceCode when we ask it for a second network connection."

   (let ((mess-name (elt vcode-req 0)) (mess-cont (elt vcode-req 1))
	 (ok-mess-cont (make-hash-table :key 'string=)))


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
)

(defun vcode-cmd-send-app-id (vcode-req)

   "Sends the unique ID received from VCode server (when opened first
network connection to it) back to the VCode server.

This allows the VCode server to know for sure that the second network
connection originates from the same Emacs instance as the first one."


   (let ((mess-cont (make-hash-table :test 'string=)))

     ;;; Then send that ID back to the server
     (cl-puthash "value" vcode-app-id mess-cont)
     (vr-send-reply (run-hook-with-args 'vr-serialize-message-hook (list "my_id_is" mess-cont)))


     ;;;
     ;;; Invoke 'vr-startup explicitly here because VCode server never sends an
     ;;; 'inialize message.
     ;;;
     (vr-startup)

   )
)

(defun vcode-wait-for-handshake ()
  "This function waits until Emacs has shaken hands with VoiceCode server
on the first socket connection. We know the handshake has happened when
Emacs has set 'vcode-app-id to a non nil value."


;  (sleep-for 30)
  (while (not vcode-app-id)
    (progn
      (sleep-for 0.1)
      )
    )
)

(defun vcode-send-kill-buffer ()
   "Sends a message to VCode server to tell it that Emacs has closed a buffer"
   (let ((mess-cont (make-hash-table :test 'string=)))
     (cl-puthash "buff_name" (buffer-name) mess-cont)
     (cl-puthash "action" "close_buff" mess-cont)
     (vr-send-cmd 
       (run-hook-with-args 
	 'vr-serialize-message-hook (list "updates" mess-cont)))
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

(defun vcode-cmd-suspendable (vcode-request)
   (let ((resp-cont (make-hash-table :test 'string=)))

     (if (string= "w32" window-system)
	 (cl-puthash "value" 0 resp-cont)
       (cl-puthash "value" 1 resp-cont)	 
     )
    (vr-send-reply 
     (run-hook-with-args 
      'vr-serialize-message-hook (list "suspendable_resp" resp-cont)))
   )
)

(defun vcode-cmd-recognition-start (vcode-request)
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
  )


(defun vcode-cmd-recognition-end (vcode-request)
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

  )


(defun vcode-cmd-active-buffer-name (vcode-request)
  (let ((mess-cont (make-hash-table :test 'string=)))
    (cl-puthash "value" (buffer-name) mess-cont)
    (vr-send-reply (run-hook-with-args 'vr-serialize-message-hook (list "active_buffer_name_resp" mess-cont)))
    )
  )


;;;
;;; Generate a hash table describing an insertion or deletion change
;;;
(defun vcode-generate-insert-change-hash (a-change)
  (let ((buff-name (nth 0 a-change))
	(deleted-start (nth 1 a-change))
	(deleted-end (nth 2 a-change))
	(inserted-text (nth 3 a-change))
	(insert-change-hash (make-hash-table :test 'string=)))

    (cl-puthash "action" "insert" insert-change-hash)
    (cl-puthash "range" 
		(list (vcode-convert-pos deleted-start 'vcode)
		      (vcode-convert-pos deleted-end 'vcode))
		insert-change-hash)
    (cl-puthash "buff_name" buff-name insert-change-hash)
    (cl-puthash "text" inserted-text insert-change-hash)

    insert-change-hash
  )
)


(defun vcode-generate-select-change-hash (a-change)
  (let ((buff-name (nth 0 a-change))
	(sel-start (nth 1 a-change))
	(sel-end (nth 2 a-change))
	(select-change-hash (make-hash-table :test 'string=))
	(range nil))
    (cl-puthash "action" "select" select-change-hash)
    (setq range (vcode-convert-range sel-start sel-end 'vcode))
    (cl-puthash "range" range select-change-hash)
    (cl-puthash "cursor_at" 1 select-change-hash)
    (cl-puthash "buff_name" buff-name select-change-hash)
    select-change-hash
  )
)


(defun vcode-generate-change-hash (a-change)

    (if (eq (nth 0 a-change) 'change-is-insert)
	(setq a-change-hash (vcode-generate-insert-change-hash (nth 1 a-change)))
      (setq a-change-hash (vcode-generate-select-change-hash (nth 1 a-change)))
    )
    a-change-hash
)

(defun vcode-serialize-changes (change-list)
  "Creates a change notification message to be sent to VCode speech server.

Argument 'change-list is a list of 5ple:
   (change-type buffer-name inserted-start inserted-end deleted-length).

If 'vr-changes-caused-by-sr-cmd is not nil, then the message must be 
formatted as a response message to SR command 'vr-changes-caused-by-sr-cmd.

Otherwise, the message must be formated as an Emacs initiated 'updates_cbk' 
message.
"

  (let ((mess "") (buff-name) (a-change) (inserted-start) (inserted-end) 
	(deleted-length) (inserted-text)
	(change-list-vcode (list)) (a-change-vcode) (a-change-action)
	(deleted-end)
	(mess-name) (mess-cont (make-hash-table :test 'string=)))


    (while change-list
      (setq a-change (car change-list))
      (setq change-list (cdr change-list))

      ;;; Generate a hashes describing this change and append it to the 
      ;;; change list destined for VCode
      (setq a-change-vcode (vcode-generate-change-hash a-change))

      (setq change-list-vcode 
	    (append change-list-vcode (list a-change-vcode)))
    )

    
    ;;; Name the message that will be sent to VCode.
    ;;; Changes generated in response to VCode request "some_command"
    ;;; -> name = "some_command_resp"
    ;;;
    ;;; Changes not generated in response to a VCode request:
    ;;; -> name = "updates_cbk"
    (if vr-changes-caused-by-sr-cmd
	(setq mess-name (format "%s_resp" vr-changes-caused-by-sr-cmd))
      (setq mess-name "updates_cbk")
      )
    (cl-puthash "updates" change-list-vcode mess-cont)

    (run-hook-with-args 
      'vr-serialize-message-hook (list mess-name mess-cont)))
)

(defun vcode-cmd-open-file (vcode-request)
  (let ((mess-cont (elt vcode-request 1)) 
	(file-name)
	(response (make-hash-table :test 'string=)))
    (setq file-name (cl-gethash "file_name" mess-cont))
    (vr-log "--** vcode-cmd-open-file: python-mode-hook =%S file-name=%S\n" file-name python-mode-hook )
    (find-file (substitute-in-file-name file-name))
    (cl-puthash "buff_name" (buffer-name) response)
    (vr-send-reply
     (run-hook-with-args 
      'vr-serialize-message-hook (list "open_file_resp" response))
    )
  )
)


(defun vcode-cmd-confirm-buffer-exists (vcode-request)
  (let ((mess-cont (elt vcode-request 1)) 
	(buffer-name)
	(response (make-hash-table :test 'string=)))

    (setq buffer-name (vcode-get-buff-name-from-message mess-cont))
    (if (get-buffer buffer-name)
	(cl-puthash "value" 1 response)
      (cl-puthash "value" 0 response))
    (vr-send-reply
     (run-hook-with-args 
      'vr-serialize-message-hook (list "confirm_buffer_exists_resp" response))
    )
  )
)


(defun vcode-cmd-list-open-buffers (vcode-request)
  (let ((mess-cont (elt vcode-request 1)) 
	(open-buffers (buffer-list))
	(buffer-names nil)
	(response (make-hash-table :test 'string=)))

    (while open-buffers
      (if (vr-activate-buffer-p (car open-buffers))
	  (setq buffer-names (append buffer-names (list (buffer-name (car open-buffers)))))
      )
      (setq open-buffers (cdr open-buffers))
      )

    (cl-puthash "value" buffer-names response)
    (vr-send-reply
     (run-hook-with-args 
      'vr-serialize-message-hook (list "list_open_buffers_resp" response))
    )
  )
)

(defun vcode-cmd-file-name (vcode-request)
  (let ((mess-cont (elt vcode-request 1)) 
	(response (make-hash-table :test 'string=))
	(buff-name) (file-name) (buff-name))
    (setq buff-name (vcode-get-buff-name-from-message mess-cont))
    (setq file-name (buffer-file-name (get-buffer buff-name)))
    (cl-puthash "value" file-name response)
    (vr-send-reply
     (run-hook-with-args 
      'vr-serialize-message-hook (list "file_name_resp" response))
    )
  )
)


;;;
;;; Kill a buffer, possibly saving it and/or asking user if she wants
;;; to save.
;;;

(defun vcode-kill-buffer (buff-name save)
  ;;; 
  ;;; kill-buffer will prompt user if buffer needs saving
  ;;;

  ;;; beg
;  (vr-log "**-- vcode-kill-buffer: sleeping for 10 secs, to make sure all the pending change notifications happen before we rename the current buffer to ignorethisfie.tmp\n")
;  (sleep-for 10)
  ;;; end

  (if (eq 0 save) 
      (progn
	(kill-buffer buff-name)
      )
  )
  (if (eq -1 save) 
      (progn
	;;;
	;;; Don't know how to kill a buffer without asking the user
	;;; if wants to save.
	;;; So save buffer under a temporary name, and then kill it.
        ;;;
	;;; Since the temporary file will be up to date, Emacs won't
	;;; query user.
	;;;
	;;; Note that we remove the 'after-change-hook before writing
	;;; to the temporary file. This is because saving to the temporary
        ;;; file caused a change to be reported on that temporary file, and
	;;; inserted in 'vr-queued-changes. But when the change queue got
	;;; cleaned up, the temporary file had been closed and Emacs was 
        ;;; freezing.
	;;;

	(write-file "ignorethisfile.tmp")
	(kill-buffer "ignorethisfile.tmp")
;        (kill-buffer buff-name)
	)
  )
  (if (eq 1 save) 
      (progn 
	(save-buffer) 
	(kill-buffer buff-name)
      )
  )
)


(defun vcode-cmd-close-buffer (vcode-request)
  (let ((mess-cont (elt vcode-request 1))
	(response (make-hash-table :test 'string=))
	(buff-name) (buff) (save))

    (cl-puthash "value" 1 response)

    (setq buff-name (vcode-get-buff-name-from-message mess-cont))
    (setq buff (get-buffer buff-name))
    (setq save (cl-gethash "save" mess-cont))

    (if (not buff)
       ;;; 'buff_name is not the name of a buffer. Maybe the name
       ;;; of a file visited by a buffer?
	(progn
	  (setq buff (find-buffer-visiting buff-name))
	)
      )

    ;;;
    ;;; Ignore VCode requests to close the minibuffer
    ;;;
    (vr-log "--** vcode-cmd-close-buffer: before testing for minbufff, buff=%S\n")
    (if buff 
	(if (not (string-match "*Minbuff-" (buffer-name buff)))
	    (progn 
	      (vr-log "--** vcode-cmd-close-buffer: closing the buffer\n")
	      (vcode-kill-buffer buff-name save)
	    )
	  (vr-log "-- ** vcode-cmd-close-buffer: this is minibuffer... not closing it\n")
	)
      (ding)
      (message (format "VR Mode: could not close buffer %S" buff-name))
      (cl-puthash "value" 0 response)
    )

    (vr-log "--** vcode-cmd-close-buffer: before send-reply\n")
    (vr-send-reply
     (run-hook-with-args 
      'vr-serialize-message-hook (list "close_buffer_resp" response))
    )
    (vr-log "--** vcode-cmd-close-buffer: after send-reply\n")
  )
)

(defun vcode-cmd-language-name (vcode-request)
  (vr-log "WARNING: function vcode-cmd-language-name not implemented!!!\n")
  )

(defun vcode-fix-pos (pos fix-for-who default-pos)

  "Fixes a cursor position received from VCode server. 

If the position is nil, then returns the current position in the current 
buffer.

Also converts from VCode's 0-based positions to Emacs 1-based positions."

  ;;;
  ;;; If nil position was received from vcode, set it to the default
  ;;; position received as argument (current cursor, end of buffer or 
  ;;; beginning of buffer). No need to convert it to 1-based 
  ;;; counting since it is already passed it in 1-based counting
  ;;;
  (if (and (eq 'emacs fix-for-who) (not pos))
      (progn
	(setq pos default-pos)
      )
    
    ;;; Else, convert non-nil position to appropriate counting base. 
    (setq pos (vcode-convert-pos pos fix-for-who)))
  pos
)

(defun vcode-fix-range (range for-who default-range)
  "Fixes a position range received from VCode server. This range
may contain nil or string values, and the 1st element may be
greater than the 2nd element. If one of the values in 'rage is nil, 
then use values in 'default-range."

  (let ((start (nth 0 range)) (end (nth 1 range)) (tmp))
    (setq start (wddx-coerce-int start))
    (setq end (wddx-coerce-int end))

    ;;;
    ;;; If nil start position was received from VCode, set it to the lower
    ;;; bound of the default range
    ;;; No need to convert it to 1-based counting because it is already
    ;;; in 1-based value.
    ;;;
    (if (and (eq 'emacs for-who) (not start))
	(setq start (nth 0 default-range))
      ;;; Else, convert start position to appropriate count base
      (setq start (vcode-convert-pos start for-who)))

    ;;;
    ;;; If nil end position was received from VCode, set it to upper bound
    ;;; of default-range.
    ;;; No need to convert it to 1-based counting because it is already
    ;;; a 1-based value.
    ;;;
    (if (and (eq 'emacs for-who) (not end))
	(setq end (nth 1 default-range))
      ;;; Else, convert end position to appropriate count base
      (setq end (vcode-convert-pos end for-who)))

    (if (> start end)
	(progn
	  (setq tmp end)
	  (setq end start)
	  (setq start end)
	  )      
      )
    (list start end)
  )
)

(defun vcode-convert-pos (pos for-who)
  "Because Emacs and VCode use a different base for counting character 
positions (Emacs starts from 1, VCode from 0), we need to convert from one
to the other"

  (if (equal for-who 'vcode)
      (progn 
	(1- pos)
      )
    (1+ pos)
    )
)

(defun vcode-convert-range (start end for-who)
  (list (vcode-convert-pos start for-who) (vcode-convert-pos end for-who))
)

(defun is-in-hash (key table)
   (not (eq (cl-gethash key table 'entrywasnotintable) 'entrywasnotintable))
)


(defun vcode-bounds-of-buff-in-message (mess)
  "Identifies the start and end of the buffer to which VCode message 
'mess applies. If no buffer listed in the message, return bounds of current 
buffer"
  (let ((buff-name))
    (save-excursion
      (setq buff-name (cl-gethash "buff_name" mess nil))
      (if buff-name
	  (set-buffer buff-name)
      )	  
      (list (point-min) (point-max))
    )
  )
)  

;;;
;;; Fix possibly nil positions in messages, and convert them between 0-based 
;;; and 1-based counting
;;;
(defun vcode-fix-positions-in-message (message fix-for-who)
   (let ((pos) (range) (default-pos))
     (dolist (position-field '("pos" "position" "start" "end")) 
       (if (is-in-hash position-field message)
	   (progn
	     (if (or (string= "pos" position-field) 
                     (string= "position" position-field))
		 (setq default-pos (point)))
	     (if (string= "start" position-field)
		 (setq default-pos 
		       (nth 0 (vcode-bounds-of-buff-in-message message)))
	     )
	     (if (string= "end" position-field)
		 (setq default-pos 
		       (nth 1 (vcode-bounds-of-buff-in-message message)))
	     )
	     (setq pos (cl-gethash position-field message))
	     (setq pos (vcode-fix-pos pos fix-for-who default-pos))
	     (cl-puthash position-field pos message)
	   )
       )
     )

     (if (is-in-hash "range" message)
	 (progn
	     (setq range (cl-gethash "range" message))
             ;;;
             ;;; Fix possibly nil positions received from VCode
             ;;;
	     (if (eq fix-for-who 'emacs)
	         (setq range (vcode-fix-range 
			      range fix-for-who 
			      (vcode-bounds-of-buff-in-message message))))
	     (cl-puthash "range" range  message)
	 )
     )
     message
  )
)

(defun vcode-make-sure-no-nil-in-selection (start end)
  "Makes sure that the selection is not 'nil"
  (if (not start) (setq start end))
  (if (not end) (setq end start))
  (list start end)
)

(defun vcode-cmd-cur-pos (vcode-request)
  (let ((mess-cont (make-hash-table :test 'string=)) (buff-name))
    (setq buff-name (vcode-get-buff-name-from-message mess-cont))
    (save-excursion
      (set-buffer buff-name)
      (cl-puthash 'value (vcode-convert-pos (point) 'vcode) mess-cont)
    )
    (vr-send-reply 
     (run-hook-with-args 
      'vr-serialize-message-hook (list "cur_pos_resp" mess-cont)))
    )
)

(defun vcode-cmd-line-num-of (vcode-request)
  (let ((mess-cont (nth 1 vcode-request))
	(response (make-hash-table :test 'string=))
	(buff-name) (line-num) (opoint))

    (setq opoint (cl-gethash "position" mess-cont))
    (setq buff-name (vcode-get-buff-name-from-message mess-cont))

    (save-excursion
      (set-buffer buff-name)
      (goto-char opoint)
      (beginning-of-line)
      (setq line-num (1+ (count-lines 1 (point))))
      )

    (cl-puthash "value" line-num response)
    (vr-send-reply 
     (run-hook-with-args 
      'vr-serialize-message-hook (list "line_num_of_resp" response)))
    )
  )


(defun vcode-cmd-get-selection (vcode-request)
  (let ((mess-cont (nth 1 vcode-request))
        (response (make-hash-table :test 'string=))
	(selection) (buff-name))
    (setq buff-name (vcode-get-buff-name-from-message mess-cont))
    (save-excursion
      (set-buffer buff-name)
      (setq selection (vcode-make-sure-no-nil-in-selection (point) (mark)))
    )
    (cl-puthash 'value 
		(list (vcode-convert-pos (nth 0 selection) 'vcode)
		      (vcode-convert-pos (nth 1 selection) 'vcode))
		response)
    (vr-send-reply 
     (run-hook-with-args 
      'vr-serialize-message-hook (list "get_selection_resp" response)))
    )
  )

(defun vcode-cmd-get-text (vcode-request)
  (let ((resp-cont (make-hash-table :test 'string=)) 
	(mess-cont (elt vcode-request 1))
	(buff-name) (start) (end)
	)
    (setq start (cl-gethash "start" mess-cont))
    (setq end (cl-gethash "end" mess-cont))
    (setq buff-name (vcode-get-buff-name-from-message mess-cont))
    (vcode-trace "vcode-cmd-get-text" "(current-buffer)=%S, buff-name=%S, start=%S, end=%S" 
		 (current-buffer) buff-name start end)

    (save-excursion
      (set-buffer buff-name)
      (cl-puthash "value" (buffer-substring start end) resp-cont)
    )

    (vr-send-reply 
     (run-hook-with-args 
      'vr-serialize-message-hook (list "get_text_resp" resp-cont)))
    )
  )


(defun vcode-cmd-get-visible (vcode-request)
  (let ((resp-cont (make-hash-table :test 'string=))
	(mess-cont (nth 1 vcode-request))
	(buff-name))
    (setq buff-name (vcode-get-buff-name-from-message mess-cont))
    (save-excursion
      (set-buffer buff-name)
      (cl-puthash 'value (vcode-convert-range (window-start) (window-end) 'vcode) resp-cont)
    )
    (vr-send-reply (run-hook-with-args 'vr-serialize-message-hook (list "get_visible_resp" resp-cont)))
    )  
  )

(defun vcode-cmd-len (vcode-request)
  (let ((resp-cont (make-hash-table :test 'string=))
	(mess-cont (nth 1 vcode-request))
	(buff-name))
    (setq buff-name (vcode-get-buff-name-from-message mess-cont))
    (save-excursion
      (set-buffer buff-name)
      (cl-puthash 'value (buffer-size) resp-cont)
    )
    (vr-send-reply (run-hook-with-args 'vr-serialize-message-hook (list "get_visible_resp" resp-cont)))
    )  
  )

(defun vcode-cmd-newline-conventions (vcode-request)
  (let ((mess-cont (make-hash-table :test 'string=)))
    (cl-puthash 'value (list "\n") mess-cont)
    (vr-send-reply (run-hook-with-args 'vr-serialize-message-hook (list "newline_conventions_resp" mess-cont)))
    )  
  )

(defun vcode-cmd-pref-newline-conventions (vcode-request)
  (let ((mess-cont (make-hash-table :test 'string=)))
    (cl-puthash 'value "\n" mess-cont)
    (vr-send-reply (run-hook-with-args 'vr-serialize-message-hook (list "pref_newline_conventions_resp" mess-cont)))
    )  
)


(defun vcode-force-cursor-and-selection-change-report (buff-name)
  "The 'after-change-functions hook only reports on insertions and
deletions in buffer. Changes in the selection and cursor position 
are not reported.

In case where we respond to VCode by just moving the cursor and/or selection,
we need to add a dummy change report to the queued changes. This dummy change just inserts a blank string over a null region (i.e., it does nothing).

This will in effect end up reporting the position of cursor and selection 
since `vr-send-queued-changes appends that information for each and every 
change reports it sends to VCode.
"
  (let ()
    (if (not buff-name) (setq buff-name (buffer-name)))
    (setq dummy-change (list buff-name ()))
  )
)

(defun vcode-cmd-set-selection (vcode-request)
  (let ((mess-cont (nth 1 vcode-request)) 
	(sel-range) (put-cursor-at) (sel-start) (sel-end)
        (buff-name))

    (setq buff-name (vcode-get-buff-name-from-message mess-cont))
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
    (condition-case err     
	(progn
	  (switch-to-buffer buff-name)
	  (goto-char sel-start)
	  (set-mark sel-start)
	  (goto-char sel-end)
	)
       ('error (error "VR Error: could not select region [%S, %S]" sel-start sel-end))
    )

    ;;;
    ;;; Selection changes do not automatically get queued to the change queue.
    ;;; Need to do so explicitely
    ;;;
    ;;; Compute final selection here as opposed to inside the 'condition-case
    ;;; statement. That way, if there are errors, we can still report
    ;;; where Emacs actually set the selection, as opposed to where we
    ;;; expected it to go.
    (vr-report-goto-select-change buff-name (mark) (point))

    (vr-send-queued-changes)
  )
)

(defun vcode-cmd-move-relative-page (vcode-request)
  (let ((mess-cont (elt vcode-request 1)) 
	(buff-name) (direction) (num))
    (setq direction (cl-gethash "direction" mess-cont))
    (setq buff-name (vcode-get-buff-name-from-message mess-cont))
    (setq num (cl-gethash "num" mess-cont))
    (set-buffer buff-name)
    (if (>= direction 0)
	(scroll-down-nomark num)
      (scroll-up-nomark num))
  )
)

(defun vcode-cmd-insert (vcode-request)
  (let ((mess-name (elt vcode-request 0)) 
	(mess-cont (elt vcode-request 1))
	(text) (range) (vr-request) 
	(delete-start) (delete-end))
	(setq text (wddx-coerce-string (cl-gethash "text" mess-cont)))
	(setq buff-name (vcode-get-buff-name-from-message mess-cont))
	(setq range (cl-gethash "range" mess-cont))
	(setq delete-start (elt range 0))
	(setq delete-end (elt range 1))

	(set-buffer buff-name)
	(kill-region delete-start delete-end)
	(set-mark nil)

        (vcode-execute-command-string text)

	(vr-send-queued-changes)
    )
)

(defun vcode-cmd-set-text (vcode-request)
  (let ((mess-name (elt vcode-request 0)) 
 	(mess-cont (elt vcode-request 1))
 	(buff-name) (text) (start) (end))

 	(setq text (wddx-coerce-string (cl-gethash "text" mess-cont)))
 	(setq buff-name (vcode-get-buff-name-from-message mess-cont))
 	(setq start (cl-gethash "start" mess-cont))
 	(setq end (cl-gethash "end" mess-cont))
        (vcode-trace "vcode-cmd-set-text" "buff-name=%S, text=%S, start=%S, end=%S\n" buff-name text start end)
	(set-buffer buff-name)
	(vcode-trace "vcode-cmd-set-text" "*** before kill-region, in buff-name, (point-min)=%S, (point-max)=%S, after-change-functions=%S, buffer contains:\n%S" (point-min) (point-max) after-change-functions (buffer-substring (point-min) (point-max)))
	(kill-region start end)
	(vcode-trace "vcode-cmd-set-text" "*** after kill-region, buffer contains\n%S" (buffer-substring (point-min) (point-max)))
	(set-mark nil)

        ;;;
	;;; We don't use 'vcode-execute-command-string because set_text message
        ;;; is used to restore a buffer to a previous state (which is
        ;;; assumed to have already been indented properly)
	(insert text)

	(vcode-trace "vcode-cmd-set-text" "*** after insert, buffer contains\n%S" (buffer-substring (point-min) (point-max)))

 	(vr-send-queued-changes)
    )
)



(defun vcode-cmd-indent (vcode-request)
  (let ((mess-name (elt vcode-request 0)) 
	(mess-cont (elt vcode-request 1))
	(range) (vr-request) (buff-name)
	(indent-start) (indent-end))

    (setq range (cl-gethash "range" mess-cont))
    (setq indent-start (elt range 0))
    (setq indent-end (elt range 1))
    (setq buff-name (vcode-get-buff-name-from-message mess-cont))


    (set-buffer buff-name)
    (vcode-indent-region indent-start indent-end)

    (vr-send-queued-changes)
  )
)


(defun vcode-cmd-decr-indent-level (vcode-request)
  (let ((mess-name (elt vcode-request 0))
	(mess-cont (elt vcode-request 1))
	(range) (levels) (vr-request) (buff-name)
	(indent-start) (indent-end))
    (setq range (cl-gethash "range" mess-cont))
    (setq indent-start (elt range 0))
    (setq indent-end (elt range 1))
    (setq levels (cl-gethash "levels" mess-cont))
    (setq buff-name (vcode-get-buff-name-from-message mess-cont))

    (vr-log "--** vcode-cmd-decr-indent-level: upon entry, (point)=%S, (mark)=%S, range=%S, levels=%S\n" (point) (mark) range levels)

    (set-buffer buff-name)
    (save-excursion
      (set-mark nil)
      (vcode-unindent-region indent-start indent-end levels) 
      (vr-log "--** vcode-cmd-decr-indent-level: upon exit, (point)=%S, (mark)=%S, buffer contains\n%S\n" (point) (mark) (buffer-substring (point-min) (point-max)))
    )

    (vr-send-queued-changes)
  )
)

(defun vcode-insert-with-autoindented-tabs-OBSOLETE (text)
   "Insert TEXT, but invoke 'indent-for-tab-command instead of inserting
tabs.
"
   (let ((before-tab) (after-tab) (tab-pos) (tab-was-found))
     (while (not (string= text ""))
       ;;;
       ;;; Find text before and after next occurence of TAB
       ;;;
       (setq tab-pos (string-match "\t" text))
       (if (not tab-pos)
	   (progn
	     (setq tab-was-found nil)
	     (setq tab-pos (length text))
	   )
	 (setq tab-was-found t)
       )
       (setq before-tab (substring text 0 tab-pos))
       (if tab-was-found 
	   (setq text (substring text (1+ tab-pos) (length text)))
	 (setq text "")
       )  

       ;;;
       ;;; Insert text before tab, and indent the tab.
       ;;;
       (insert before-tab)
       (if tab-was-found (indent-for-tab-command))
     )
   )
)

(defun vcode-indent-region (start end)
  ;;;
  ;;; For some reason, when I invoke (indent-region start end) it doesn't 
  ;;; work. If I mark the region and then invoke (indent-region) without
  ;;; arguments, it doesn't work either. The only way I found to make it
  ;;; work is to mark the region, and then simulate an interactive call to
  ;;; indent-region
  ;;; 
  (save-excursion
    (set-mark start)
    (goto-char end)
    (call-interactively 'indent-region)
;    (indent-region start end)
  )
)

(defun vcode-unindent-region (start end n-levels)
  "Deindents region from START to END by N-LEVELS levels."
  (let (end-line)
    (vr-log "--** vcode-unindent-region: start=%S, end=%S, n-levels=%S, (point)=%S, (mark)=%S, buffer content is\n%S\n" start end n-levels (point) (mark) (buffer-substring (point-min) (point-max)))
    (for-lines-in-region-do start end 'vcode-unindent-line (list n-levels))
    (vr-log "-- vcode-unindent-region: upon exit, (point)=%S, (mark)=%S, buffer contains: \n%S\n" (point) (mark) (buffer-substring (point-min) (point-max)))
  )
)

(defun vcode-unindent-line (n-levels)
  (interactive "nNumber of levels: ")
  (let ((counter 0) (start-of-line))
     (vr-log "--** vcode-unindent-line: upon entry, n-levels=%S, (point)=%S, (mark)=%S, buffer contains: \n%S\n" n-levels (point) (mark) (buffer-substring (point-min) (point-max)))
      ;;;
      ;;; Move to the first non-blank character on the line, then simulate the
      ;;; backspace key multiple times.
      ;;;
      (beginning-of-line)
      (setq start-of-line (point))
      (while (and (looking-at " ") (< (point) (point-max)))
        (forward-char-nomark 1)
        )

      ;;;
      ;;; Don't backspace if empty line, because that will delete the line 
      ;;; instead of deindenting.
      ;;;
      (if (not (or (eq start-of-line (point)) (eq 1 (point))))
          (progn
           (setq counter 0)
	   (while (< counter n-levels)
	     (save-excursion
             ;;; Execute a command string containing just the backspace key
	       (vcode-execute-command-string "\177")
	     )
             (setq counter (1+ counter))
           )
           )
      )

     (vr-log "--** vcode-unindent-line: upon exit, n-levels=%S, (point)=%S, (mark)=%S, buffer contains: \n%S\n" n-levels (point) (mark) (buffer-substring (point-min) (point-max)))
   )
)

(defun what-line (pos)
   (let ((line-num))
     (setq line-num (count-lines (point-min) pos))
     (save-excursion
       (goto-char pos)
       (if (bolp)
           (setq line-num (1+ line-num))
       )
     )
     line-num
   )
)

(defun for-lines-in-region-do (start end do-this args)
  (let ((start-line) (end-line) (keep-going) (current-line))
    (vr-log "--** for-lines-in-region-do: upon entry, (point)=%S, (mark)=%S, buffer contains:\n%S\n" (point) (mark) (buffer-substring (point-min) (point-max)))
    (save-excursion
       (setq end-line (what-line end))
       (message "-- end-line=%S\n" end-line)
       (goto-char start)
       (setq keep-going t)
       (while keep-going
         (message "-- processing line: current-line=%S, (point)=%S" (what-line (point)) (point))
         (apply do-this args)
	 (setq current-line (what-line (point)))
         (if (<  current-line end-line)
	     (next-line 1)
	   (setq keep-going nil)
	 )
       )
       (vr-log "--** for-lines-in-region-do: before exiting save-excursion, (point)=%S, (mark)=%S, buffer contains:\n%S\n" (point) (mark) (buffer-substring (point-min) (point-max)))
    )
    (vr-log "--** for-lines-in-region-do: upon exit, (point)=%S, (mark)=%S, buffer contains:\n%S\n" (point) (mark) (buffer-substring (point-min) (point-max)))
  )
)


(defun vcode-cmd-delete (vcode-request)
  (let ((mess-name (elt vcode-request 0)) 
	(mess-cont (elt vcode-request 1))
	(text) (range) (vr-request) 
	(delete-start) (delete-end) (buff-name))

	(setq buff-name (vcode-get-buff-name-from-message mess-cont))
	(setq range (cl-gethash "range" mess-cont))
	(setq delete-start (elt range 0))
	(setq delete-end (elt range 1))
	(set-buffer buff-name)
	(kill-region delete-start delete-end)
        (set-mark nil)

	(vr-send-queued-changes)
    )
)



(defun vcode-cmd-goto (vcode-request)
  (let ((mess-cont (nth 1 vcode-request))
	(pos) (buff-name) (final-pos))
    (setq pos (cl-gethash "pos" mess-cont))
    (setq buff-name (vcode-get-buff-name-from-message mess-cont))
    (condition-case err     
	(progn 
	  (switch-to-buffer buff-name)
	  (goto-char pos)
	)

      ('error (error "VR Error: could not go to position %S" pos))
    )

    ;;;
    ;;; Compute final position here instead of inside the 'condition-case 
    ;;; statement. That way, if there were some errors, we can still
    ;;; report where the cursor actually went (as opposed to where we 
    ;;; expected it to go).
    ;;;
    (switch-to-buffer buff-name)
    (setq final-pos (point))

    ;;;
    ;;; Cursor changes do not automatically get queued to the change queue.
    ;;; Need to do so explicitely
    ;;;
    (vr-report-goto-select-change buff-name final-pos final-pos)

    (vr-send-queued-changes)

  )
)

(defun vcode-cmd-goto-line (vcode-request)
  (let ((mess-cont (nth 1 vcode-request))
	(line-num) (go-where) (buff-name) (final-pos))
    (setq line-num (cl-gethash "linenum" mess-cont))
    (setq go-where (cl-gethash "where" mess-cont))
    (setq buff-name (vcode-get-buff-name-from-message mess-cont))
    (condition-case err     
	(progn 
	  (switch-to-buffer buff-name)
	  (goto-line line-num)
	  (if (= -1 go-where) 
	      (beginning-of-line)
	    (end-of-line)
	  )
	)
      ('error (error "VR Error: could not go to line %S" line-num))
    )

    ;;;
    ;;; Compute final position here instead of inside the 'condition-case 
    ;;; statement. That way, if there were some errors, we can still
    ;;; report where the cursor actually went (as opposed to where we 
    ;;; expected it to go).
    ;;;
    (switch-to-buffer buff-name)
    (setq final-pos (point))

    ;;;
    ;;; Cursor changes do not automatically get queued to the change queue.
    ;;; Need to do so explicitely
    ;;;
    (vr-report-goto-select-change buff-name final-pos final-pos)

    (vr-send-queued-changes)

  )
)

(defun vcode-cmd-mediator-closing (vcode-request)
  (vr-mode-activate 'vcode)
)