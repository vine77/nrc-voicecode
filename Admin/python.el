;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Useful macros for writing Python code
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


;;;
;;; Set the string of blank spaces used to indent by one level
;;;
(setq py-indent-padding
      (progn
	(let ((counter py-indent-offset) (buff ""))
	  (while (> counter 0)
	    (setq buff (concat buff " "))
	    (setq counter (- counter 1))
	    )
	  buff
	  )
 	)
)
(setq py-indent-padding2 (concat py-indent-padding py-indent-padding))
(setq py-indent-padding3 (concat py-indent-padding py-indent-padding2))


(defun pym (name arg-string)
  (interactive "sName: \nsArguments: ")
  "Inserts template code for a python method."

  (py-method name arg-string 1)
)
(defun pyf (name arg-string)
  (interactive "sName: \nsArguments: ")
  "Inserts template code for a python function."

  (py-method name arg-string nil)
)
(defun py-method (name arg-string is-method)

  (let ((arg-list nil) (padding1 "") (an-arg nil) (arg-num nil) 
	(desc-start nil) (desc-end nil))
    
    ;;;
    ;;; Determine list of arguments (check if 1st argument is self)
    ;;;
    (setq arg-list (split-string arg-string "[ ,]+"))
    (if (string= (elt arg-list 0) "self")
	(progn
	  (setq arg-list (cdr arg-list))
	  ;;; Interpret this as a method, even if it was called with 
	  ;;; is-method set to nil
	  (setq is-method 1)
	  )
	)

    ;;;
    ;;; Methods are indented, but functions aren't
    ;;;
    (if is-method (setq padding1 py-indent-padding))
    (setq padding2 (concat padding1 py-indent-padding))


    ;;;
    ;;; Print signature of method
    ;;;
    (beginning-of-line)    
    (insert (concat padding1 "def " name "("))
    (if is-method (insert "self"))
    (setq arg-num 0)
     (while (< arg-num (length arg-list))
       (if (or (> arg-num 0) is-method) (insert ", "))
       (insert (elt arg-list arg-num))
       (setq arg-num (+ 1 arg-num))
       )
    (insert "):\n")

    ;;;
    ;;; Print documentation for method and its arguments
    ;;;
    (insert (concat padding2 "\"\"\""))
    (setq desc-start (point))
    (insert (concat "... Terse 1 line description ...\n\n" padding2 "... Detailed description ..."))
    (setq desc-end (point))
    (insert (concat "\n\n" padding2 "**INPUTS**\n\n"))
   
    
    (mapcar #'(lambda (an-arg) (insert (concat padding2 "*untyped* " an-arg " -- undocumented \n\n"))) arg-list)
    (if (eq 0 (length arg-list)) (insert (concat padding2 "*none* -- \n\n")))
    
    (insert (concat "\n" padding2 "**OUTPUTS**\n\n" padding2 "*none* -- \n" padding2 "\"\"\""))

    ;;;
    ;;; Move cursor to short description
    ;;;
    (set-mark desc-end)
    (goto-char desc-start)
    )
)


(defun pyc ()
  (interactive)
  (call-interactively `py-class)
)
 (defun py-class (class-name super-classes)
   (interactive "sClass Name: \nsSuperclasses: ")
   (let ((descr-start nil) (descr-end nil))
     (beginning-of-line)
     (insert (concat "class " class-name))
     (if (not (string= "" super-classes)) (insert (concat "(" super-classes ")")))
     (insert (concat ":\n" py-indent-padding "\"\"\""))
     (setq descr-start (point))
     (insert (concat "... Terse 1 line description here ...\n\n" py-indent-padding "... Detailed description here ..."))
     (setq descr-end (point))
     (insert (concat "\n" py-indent-padding "\"\"\""))
    
     ;;;
     ;;; Mark description placeholders
     ;;;
     (set-mark descr-end)
     (goto-char descr-start)
     )
)
