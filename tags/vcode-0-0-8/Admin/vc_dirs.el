;;;
;;; Shortcuts to move to different directories of VoiceCode
;;;

(defun vchome ()
  (interactive)
  (cd (substitute-in-file-name "$VCODE_HOME/"))
)

(defun vcmed ()
  (interactive)
  (cd (substitute-in-file-name "$VCODE_HOME/Mediator"))
)

(defun vcadmin ()
  (interactive)
  (cd (substitute-in-file-name "$VCODE_HOME/Admin"))
)

(defun vcdata ()
  (interactive)
  (cd (substitute-in-file-name "$VCODE_HOME/Data"))
)

(defun vctdata ()
  (interactive)
  (cd (substitute-in-file-name "$VCODE_HOME/Data/TestData"))
)

(defun vcbench ()
  (interactive)
  (cd (substitute-in-file-name "$VCODE_HOME/Data/Benchmark"))
)

(defun vcdoc ()
  (interactive)
  (cd (substitute-in-file-name "$VCODE_HOME/Doc"))
)


