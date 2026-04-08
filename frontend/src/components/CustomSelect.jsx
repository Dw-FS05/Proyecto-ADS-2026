import { useState, useRef, useEffect } from 'react'
import './CustomSelect.css'

export default function CustomSelect({ value, onChange, options, className = '' }) {
  const [open, setOpen] = useState(false)
  const ref = useRef(null)

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (ref.current && !ref.current.contains(e.target)) setOpen(false)
    }
    document.addEventListener('click', handleClickOutside)
    return () => document.removeEventListener('click', handleClickOutside)
  }, [])

  const selectedLabel = options.find((o) => o.value === value)?.label || value

  return (
    <div ref={ref} className={`custom-select ${className} ${open ? 'open' : ''}`}>
      <button
        type="button"
        className="custom-select-trigger"
        onClick={() => setOpen(!open)}
        tabIndex={0}
      >
        <span>{selectedLabel}</span>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M6 9l6 6 6-6" />
        </svg>
      </button>
      {open && (
        <div className="custom-select-dropdown">
          {options.map((opt) => (
            <div
              key={opt.value}
              role="button"
              tabIndex={0}
              className={`custom-select-option ${opt.value === value ? 'selected' : ''}`}
              onClick={() => {
                onChange(opt.value)
                setOpen(false)
              }}
              onKeyDown={(e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                  e.preventDefault()
                  onChange(opt.value)
                  setOpen(false)
                }
              }}
            >
              {opt.label}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
