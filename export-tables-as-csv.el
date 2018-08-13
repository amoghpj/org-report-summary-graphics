(require 'org)


(defun my-tbl-export (name)
  "Search for table named `NAME` and export."
  (interactive "s")
  (show-all)
  (let ((case-fold-search t))
    (if (search-forward-regexp (concat "#\\+NAME: +" name) nil t)
    (progn
      (next-line)
      (next-line)
      (next-line)
      (org-table-export (format "%s.csv" name+org-time-stamp) "orgtbl-to-csv")))))
